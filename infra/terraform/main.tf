terraform {
  required_version = ">= 1.8.4"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.50"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }

  backend "s3" {
    bucket         = "normative-rag-terraform-state"
    key            = "prod/terraform.tfstate"
    region         = "us-east-1"
    encrypt        = true
    dynamodb_table = "terraform-state-lock"
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Project         = "normative-rag-system"
      Environment     = var.environment
      ManagedBy       = "terraform"
      CostCenter      = "Cumplimiento"
      DataClassification = "internal"
    }
  }

  skip_credentials_validation = false
  skip_requesting_account_id  = false
  skip_metadata_api_check     = true
}

variable "aws_region" {
  description = "Región de AWS donde se desplegará la infraestructura"
  type        = string
  default     = "us-east-1"

  validation {
    condition     = contains(["us-east-1", "us-west-2", "eu-west-1"], var.aws_region)
    error_message = "Región no soportada. Usar us-east-1, us-west-2 o eu-west-1"
  }
}

variable "environment" {
  description = "Entorno de despliegue (dev, staging, prod)"
  type        = string
  default     = "prod"

  validation {
    condition     = contains(["dev", "staging", "prod"], var.environment)
    error_message = "Entorno debe ser: dev, staging o prod"
  }
}

variable "lambda_timeout" {
  description = "Timeout en segundos para la función Lambda"
  type        = number
  default     = 30

  validation {
    condition     = var.lambda_timeout >= 3 && var.lambda_timeout <= 900
    error_message = "Timeout debe estar entre 3 y 900 segundos"
  }
}

variable "lambda_memory" {
  description = "Memoria en MB para la función Lambda"
  type        = number
  default     = 512

  validation {
    condition     = var.lambda_memory >= 128 && var.lambda_memory <= 10240
    error_message = "Memoria debe estar entre 128 y 10240 MB"
  }
}

variable "bedrock_model_id" {
  description = "ID del modelo de Bedrock a utilizar"
  type        = string
  default     = "anthropic.claude-3-sonnet-20240229-v1:0"
}

variable "opensearch_collection_name" {
  description = "Nombre de la colección de OpenSearch Serverless"
  type        = string
  default     = "normative-rag-vectors"
}

locals {
  function_name      = "normative-rag-api-${var.environment}"
  api_name           = "normative-rag-api-${var.environment}"
  s3_documents_bucket = "normative-rag-documents-${var.environment}-${data.aws_caller_identity.current.account_id}"
  dynamodb_table_name = "normative-rag-evaluations-${var.environment}"
  log_group_name     = "/aws/lambda/${local.function_name}"
  common_tags = merge(
    var.common_tags,
    {
      Name        = local.function_name
      Environment = var.environment
    }
  )
}

data "aws_caller_identity" "current" {}

data "aws_region" "current" {}

data "aws_ami" "amazon_linux" {
  most_recent = true
  owners      = ["amazon"]

  filter {
    name   = "name"
    values = ["al2023-ami-*-x86_64"]
  }
}

resource "random_id" "bucket_suffix" {
  byte_length = 8
}

resource "aws_s3_bucket" "documents" {
  bucket = "normative-rag-documents-${var.environment}-${random_id.bucket_suffix.hex}"

  tags = local.common_tags
}

resource "aws_s3_bucket_versioning" "documents_versioning" {
  bucket = aws_s3_bucket.documents.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "documents_encryption" {
  bucket = aws_s3_bucket.documents.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "documents_block" {
  bucket = aws_s3_bucket.documents.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}

resource "aws_dynamodb_table" "evaluations" {
  name           = local.dynamodb_table_name
  billing_mode   = "PAY_PER_REQUEST"
  hash_key       = "query_id"
  range_key      = "timestamp"

  attribute {
    name = "query_id"
    type = "S"
  }

  attribute {
    name = "timestamp"
    type = "S"
  }

  attribute {
    name = "user_id"
    type = "S"
  }

  global_secondary_index {
    name            = "user-timestamp-index"
    hash_key        = "user_id"
    range_key       = "timestamp"
    projection_type = "ALL"
  }

  ttl {
    attribute_name = "ttl"
    enabled        = true
  }

  tags = local.common_tags
}

resource "aws_iam_role" "lambda_exec" {
  name = "normative-rag-lambda-role-${var.environment}"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      }
    ]
  })

  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_policy" "lambda_permissions" {
  name = "normative-rag-lambda-permissions-${var.environment}"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "bedrock:InvokeModel",
          "bedrock:InvokeModelWithResponseStream",
          "bedrock:GetFoundationModel",
          "bedrock:ListFoundationModels"
        ]
        Resource = "arn:aws:bedrock:${data.aws_region.current.name}::foundation-model/*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetObject",
          "s3:ListBucket",
          "s3:GetBucketLocation"
        ]
        Resource = [
          aws_s3_bucket.documents.arn,
          "${aws_s3_bucket.documents.arn}/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "dynamodb:GetItem",
          "dynamodb:PutItem",
          "dynamodb:Query",
          "dynamodb:Scan",
          "dynamodb:UpdateItem",
          "dynamodb:DeleteItem"
        ]
        Resource = [
          aws_dynamodb_table.evaluations.arn,
          "${aws_dynamodb_table.evaluations.arn}/index/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "aoss:APIAccess",
          "aoss:ListCollections",
          "aoss:DescribeCollection"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "logs:CreateLogGroup",
          "logs:CreateLogStream",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:log-group:${local.log_group_name}*"
      },
      {
        Effect = "Allow"
        Action = [
          "cloudwatch:PutMetricData",
          "cloudwatch:GetMetricStatistics"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = "secretsmanager:GetSecretValue"
        Resource = "arn:aws:secretsmanager:${data.aws_region.current.name}:${data.aws_caller_identity.current.account_id}:secret:normative-rag/*"
      }
    ]
  })

  tags = local.common_tags
}

resource "aws_iam_role_policy_attachment" "lambda_custom" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = aws_iam_policy.lambda_permissions.arn
}

data "archive_file" "lambda_payload" {
  type        = "zip"
  source_dir  = "${path.module}/../../deployment/package"
  output_path = "${path.module}/lambda_function_payload.zip"

  excludes = [
    ".pytest_cache",
    "__pycache__",
    "*.pyc",
    ".env",
    ".git"
  ]
}

resource "aws_lambda_function" "api" {
  filename         = data.archive_file.lambda_payload.output_path
  function_name    = local.function_name
  role            = aws_iam_role.lambda_exec.arn
  handler         = "app.main.handler"
  source_code_hash = data.archive_file.lambda_payload.output_base64sha256

  runtime = "python3.13"

  memory_size = var.lambda_memory
  timeout     = var.lambda_timeout

  environment {
    variables = {
      AWS_REGION                = data.aws_region.current.name
      ENVIRONMENT               = var.environment
      BEDROCK_MODEL_ID          = var.bedrock_model_id
      DOCUMENTS_BUCKET          = aws_s3_bucket.documents.id
      EVALUATIONS_TABLE         = aws_dynamodb_table.evaluations.name
      OPENSEARCH_COLLECTION     = var.opensearch_collection_name
      LOG_LEVEL                 = var.environment == "prod" ? "INFO" : "DEBUG"
      MAX_TOKENS                = "2048"
      TEMPERATURE               = "0.7"
      TOP_P                     = "0.9"
    }
  }

  reserved_concurrent_executions = var.environment == "prod" ? 100 : -1

  tracing_config {
    mode = "Active"
  }

  tags = local.common_tags

  lifecycle {
    ignore_changes = [last_modified]
  }
}

resource "aws_lambda_permission" "api_gateway" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.api.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_api_gateway_rest_api.api.execution_arn}/*/*"
}

resource "aws_api_gateway_rest_api" "api" {
  name        = local.api_name
  description = "API para consultas normativas con modelos generativos"

  endpoint_configuration {
    types = ["REGIONAL"]
  }

  tags = local.common_tags
}

resource "aws_api_gateway_resource" "proxy" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  parent_id   = aws_api_gateway_rest_api.api.root_resource_id
  path_part   = "{proxy+}"
}

resource "aws_api_gateway_method" "proxy_any" {
  rest_api_id   = aws_api_gateway_rest_api.api.id
  resource_id   = aws_api_gateway_resource.proxy.id
  http_method   = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_resource.proxy.id
  http_method = aws_api_gateway_method.proxy_any.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.api.invoke_arn

  cache_namespace = aws_api_gateway_resource.proxy.id
}

resource "aws_api_gateway_method" "root_any" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_rest_api.api.root_resource_id
  http_method = "ANY"
  authorization = "NONE"
}

resource "aws_api_gateway_integration" "lambda_root" {
  rest_api_id = aws_api_gateway_rest_api.api.id
  resource_id = aws_api_gateway_rest_api.api.root_resource_id
  http_method = aws_api_gateway_method.root_any.http_method

  integration_http_method = "POST"
  type                    = "AWS_PROXY"
  uri                     = aws_lambda_function.api.invoke_arn
}

resource "aws_api_gateway_deployment" "api" {
  rest_api_id = aws_api_gateway_rest_api.api.id

  depends_on = [
    aws_api_gateway_integration.lambda,
    aws_api_gateway_integration.lambda_root
  ]

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_api_gateway_stage" "prod" {
  deployment_id = aws_api_gateway_deployment.api.id
  rest_api_id   = aws_api_gateway_rest_api.api.id
  stage_name    = var.environment

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gateway.arn
    format         = "$context.requestId: $context.endpoint $context.httpMethod $context.status $context.responseLatency $context.requestTime"
  }

  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "api_gateway" {
  name              = "/aws/apigateway/${aws_api_gateway_rest_api.api.name}"
  retention_in_days = var.environment == "prod" ? 30 : 7

  tags = local.common_tags
}

resource "aws_cloudwatch_log_group" "lambda" {
  name              = local.log_group_name
  retention_in_days = var.environment == "prod" ? 30 : 7

  tags = local.common_tags
}

resource "aws_lambda_alias" "prod" {
  name             = "prod"
  function_name    = aws_lambda_function.api.function_name
  function_version = "$LATEST"

  lifecycle {
    create_before_destroy = true
  }
}

resource "aws_cloudwatch_metric_alarm" "lambda_errors" {
  alarm_name          = "${local.function_name}-errors"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "Errors"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = "10"
  alarm_description   = "Alarm when Lambda function has errors"

  dimensions = {
    FunctionName = aws_lambda_function.api.function_name
  }

  alarm_actions = [aws_sns_topic.alerts.arn]
  ok_actions    = [aws_sns_topic.alerts.arn]

  tags = local.common_tags
}

resource "aws_cloudwatch_metric_alarm" "lambda_throttles" {
  alarm_name          = "${local.function_name}-throttles"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "Throttles"
  namespace           = "AWS/Lambda"
  period              = "300"
  statistic           = "Sum"
  threshold           = "5"
  alarm_description   = "Alarm when Lambda function is throttled"

  dimensions = {
    FunctionName = aws_lambda_function.api.function_name
  }

  alarm_actions = [aws_sns_topic.alerts.arn]

  tags = local.common_tags
}

resource "aws_sns_topic" "alerts" {
  name = "normative-rag-alerts-${var.environment}"

  tags = local.common_tags
}

resource "aws_sns_topic_subscription" "alerts_email" {
  topic_arn = aws_sns_topic.alerts.arn
  protocol  = "email"
  endpoint  = var.alert_email
}

variable "alert_email" {
  description = "Email para recibir alertas del sistema"
  type        = string
  default     = "alertas-cumplimiento@empresa.com"
}

variable "common_tags" {
  description = "Tags comunes para todos los recursos"
  type        = map(string)
  default     = {}
}

output "api_endpoint" {
  description = "Endpoint de la API REST"
  value       = "${aws_api_gateway_stage.prod.invoke_url}"
}

output "lambda_function_name" {
  description = "Nombre de la función Lambda"
  value       = aws_lambda_function.api.function_name
}

output "documents_bucket" {
  description = "Nombre del bucket S3 para documentos"
  value       = aws_s3_bucket.documents.id
}

output "evaluations_table" {
  description = "Nombre de la tabla DynamoDB para evaluaciones"
  value       = aws_dynamodb_table.evaluations.name
}

output "lambda_role_arn" {
  description = "ARN del rol de ejecución de Lambda"
  value       = aws_iam_role.lambda_exec.arn
}