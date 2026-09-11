"""Cliente para interactuar con AWS Bedrock, manejando autenticación y configuración de sesiones."""

import logging
from typing import Any, Literal

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, BotoCoreError
from langchain_aws import ChatBedrock

from app.config.settings import get_settings, Settings

logger = logging.getLogger(__name__)

AWS_REGION_DEFAULT = "us-east-1"
MAX_RETRIES = 3
TIMEOUT_SECONDS = 30


class BedrockClientError(Exception):
    """Excepción específica para errores del cliente Bedrock."""

    def __init__(self, message: str, error_code: str | None = None):
        super().__init__(message)
        self.error_code = error_code


class AWSBedrockClient:
    """Cliente para interactuar con AWS Bedrock y obtener modelos de lenguaje."""

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self._session = None
        self._client = None
        self._chat_model = None
        self._region = self.settings.aws_region or AWS_REGION_DEFAULT
        logger.info(f"AWSBedrockClient inicializado para región: {self._region}")

    def _get_boto3_session(self) -> boto3.Session:
        """Obtiene o crea una sesión de boto3 con las credenciales configuradas."""
        if self._session is not None:
            return self._session

        credentials = self._get_credentials()
        self._session = boto3.Session(
            aws_access_key_id=credentials.get("aws_access_key_id"),
            aws_secret_access_key=credentials.get("aws_secret_access_key"),
            aws_session_token=credentials.get("aws_session_token"),
            region_name=self._region,
        )
        logger.debug("Sesión de boto3 creada exitosamente")
        return self._session

    def _get_credentials(self) -> dict[str, str | None]:
        """Obtiene las credenciales desde la configuración."""
        aws_creds = get_settings().get_aws_credentials()
        return {
            "aws_access_key_id": aws_creds.get("access_key"),
            "aws_secret_access_key": aws_creds.get("secret_key"),
            "aws_session_token": aws_creds.get("session_token"),
        }

    def get_bedrock_client(self) -> Any:
        """Obtiene el cliente de Bedrock de bajo nivel."""
        if self._client is not None:
            return self._client

        session = self._get_boto3_session()
        retry_config = Config(
            retries={"max_attempts": MAX_RETRIES, "mode": "standard"},
            connect_timeout=TIMEOUT_SECONDS,
            read_timeout=TIMEOUT_SECONDS,
        )

        try:
            self._client = session.client("bedrock-runtime", config=retry_config)
            logger.info("Cliente de Bedrock creado exitosamente")
        except (ClientError, BotoCoreError) as e:
            logger.error(f"Error al crear cliente de Bedrock: {e}")
            raise BedrockClientError(
                f"No se pudo crear el cliente de Bedrock: {str(e)}",
                error_code="BEDROCK_CLIENT_INIT_ERROR",
            ) from e

        return self._client

    def get_chat_model(
        self,
        model_id: str | None = None,
        model_kwargs: dict[str, Any] | None = None,
    ) -> ChatBedrock:
        """Obtiene un modelo de chat de Bedrock configurado.

        Args:
            model_id: Identificador del modelo (por defecto, el configurado en settings).
            model_kwargs: Parámetros adicionales para el modelo.

        Returns:
            Instancia de ChatBedrock configurada.
        """
        if self._chat_model is not None and model_id is None:
            return self._chat_model

        actual_model_id = model_id or self.settings.bedrock_model_id
        if not actual_model_id:
            raise BedrockClientError(
                "No se ha especificado un model_id para Bedrock",
                error_code="MISSING_MODEL_ID",
            )

        actual_kwargs = model_kwargs or {}
        if self.settings.bedrock_temperature is not None:
            actual_kwargs["temperature"] = self.settings.bedrock_temperature
        if self.settings.bedrock_max_tokens is not None:
            actual_kwargs["max_tokens"] = self.settings.bedrock_max_tokens

        try:
            self._chat_model = ChatBedrock(
                client=self.get_bedrock_client(),
                model_id=actual_model_id,
                model_kwargs=actual_kwargs,
            )
            logger.info(f"Modelo de chat Bedrock cargado: {actual_model_id}")
        except Exception as e:
            logger.error(f"Error al cargar modelo de Bedrock: {e}")
            raise BedrockClientError(
                f"Error al cargar el modelo {actual_model_id}: {str(e)}",
                error_code="MODEL_LOAD_ERROR",
            ) from e

        return self._chat_model

    def validate_connection(self) -> bool:
        """Valida que la conexión a Bedrock esté configurada correctamente.

        Returns:
            True si la conexión es válida, False en caso contrario.
        """
        try:
            client = self.get_bedrock_client()
            client.list_foundation_models()
            logger.info("Conexión a Bedrock validada exitosamente")
            return True
        except Exception as e:
            logger.warning(f"Validación de conexión a Bedrock falló: {e}")
            return False

    def close(self) -> None:
        """Cierra los recursos del cliente."""
        self._client = None
        self._chat_model = None
        self._session = None
        logger.info("Recursos de AWSBedrockClient liberados")


def get_bedrock_client(settings: Settings | None = None) -> AWSBedrockClient:
    """Factoría para obtener una instancia de AWSBedrockClient.

    Args:
        settings: Configuración del sistema.

    Returns:
        Instancia configurada de AWSBedrockClient.
    """
    return AWSBedrockClient(settings)