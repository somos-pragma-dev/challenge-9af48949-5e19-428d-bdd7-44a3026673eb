# Stage 1: Base - Python runtime optimized for ML workloads
FROM python:3.13-slim-bookworm AS base

# Install system dependencies for ML libraries and AWS CLI
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    git \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set Python optimized settings
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONFAULTHANDLER=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Set working directory
WORKDIR /app

# Install AWS CLI v2 for infrastructure management
RUN curl -s "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip" && \
    unzip -q awscliv2.zip && \
    ./aws/install && \
    rm -rf awscliv2.zip aws

# Stage 2: Dependencies - Install Python packages
FROM base AS deps

WORKDIR /app

# Copy dependency files
COPY pyproject.toml ./pyproject.toml

# Install Python dependencies with pip
RUN pip install --no-cache-dir \
    fastapi==0.115.0 \
    uvicorn==0.30.1 \
    langchain==0.2.5 \
    langchain-aws==0.1.5 \
    langgraph==0.0.48 \
    pydantic==2.7.1 \
    boto3==1.34.123 \
    numpy==1.26.4 \
    pandas==2.2.2 \
    python-dotenv==1.0.1

# Stage 3: Application - Production image
FROM base AS production

WORKDIR /app

# Copy installed dependencies from deps stage
COPY --from=deps /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=deps /usr/local/bin /usr/local/bin

# Copy application code
COPY app/ ./app/
COPY pyproject.toml ./pyproject.toml

# Create non-root user for security
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app

USER appuser

# Expose FastAPI port
EXPOSE 8000

# Health check configuration
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Environment variables for production
ENV PYTHON_ENV=production \
    LOG_LEVEL=INFO

# Run FastAPI with uvicorn
# Using multiple workers for production workloads
CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]

# Stage 4: Development - Local development with hot reload
FROM base AS development

WORKDIR /app

# Install all dependencies including dev
RUN pip install --no-cache-dir \
    fastapi==0.115.0 \
    uvicorn==0.30.1 \
    langchain==0.2.5 \
    langchain-aws==0.1.5 \
    langgraph==0.0.48 \
    pydantic==2.7.1 \
    boto3==1.34.123 \
    numpy==1.26.4 \
    pandas==2.2.2 \
    python-dotenv==1.0.1 \
    pytest==8.2.0 \
    httpx==0.27.0

# Copy application code
COPY app/ ./app/
COPY pyproject.toml ./pyproject.toml

# Install development tools
RUN pip install --no-cache-dir pytest-asyncio pytest-cov

# Environment for development
ENV PYTHON_ENV=development \
    LOG_LEVEL=DEBUG

EXPOSE 8000

# Run with hot reload enabled
CMD ["uvicorn", "app.main:create_app", "--factory", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Stage 5: Testing - Run tests in isolated environment
FROM deps AS test

WORKDIR /app

# Copy test files
COPY tests/ ./tests/
COPY app/ ./app/

# Run pytest with coverage
CMD ["pytest", "-q", "--tb=short", "--cov=app", "--cov-report=xml", "tests/"]

# Build instructions for multi-stage builds:
# docker build --target production -t normative-rag:prod .
# docker build --target development -t normative-rag:dev .
# docker build --target test -t normative-rag:test .

# Runtime environment variables (set at container runtime):
# AWS_ACCESS_KEY_ID - AWS credentials for Bedrock access
# AWS_SECRET_ACCESS_KEY - AWS credentials for Bedrock access
# AWS_REGION - AWS region (default: us-east-1)
# S3_BUCKET_NAME - S3 bucket for document storage
# EMBEDDING_MODEL_ID - Bedrock embedding model ID
# GENERATION_MODEL_ID - Bedrock generation model ID
# VECTOR_DB_HOST - Vector database host
# VECTOR_DB_PORT - Vector database port
# LOG_LEVEL - Logging level (DEBUG, INFO, WARNING, ERROR)