import os
from functools import lru_cache
from typing import Optional

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Configuración centralizada del sistema de respuestas normativas."""
    
    app_name: str = Field(
        default="normative-rag-system",
        description="Nombre de la aplicación",
    )
    debug: bool = Field(
        default=False,
        description="Modo de depuración",
    )
    host: str = Field(
        default="0.0.0.0",
        description="Host donde se ejecuta el servidor",
    )
    port: int = Field(
        default=8000,
        description="Puerto del servidor",
    )
    log_level: str = Field(
        default="INFO",
        description="Nivel de logging",
    )
    
    aws_region: str = Field(
        default="us-east-1",
        description="Región de AWS",
    )
    bedrock_model_id: str = Field(
        default="anthropic.claude-3-sonnet-20240229-v1:0",
        description="ID del modelo Bedrock",
    )
    bedrock_max_tokens: int = Field(
        default=4096,
        description="Máximo de tokens en la respuesta",
    )
    bedrock_temperature: float = Field(
        default=0.7,
        description="Temperatura del modelo",
    )
    bedrock_top_p: float = Field(
        default=0.9,
        description="Parámetro top-p del modelo",
    )
    
    max_response_tokens: int = Field(
        default=2048,
        description="Límite de tokens para respuestas",
    )
    max_context_tokens: int = Field(
        default=8192,
        description="Máximo de tokens en el contexto",
    )
    retrieval_top_k: int = Field(
        default=5,
        description="Número de documentos a recuperar",
    )
    
    normative_repo_type: str = Field(
        default="s3",
        description="Tipo de repositorio de normativas",
    )
    normative_bucket: Optional[str] = Field(
        default=None,
        description="Bucket S3 con normativas",
    )
    normative_local_path: Optional[str] = Field(
        default=None,
        description="Ruta local para normativas (desarrollo)",
    )
    
    vector_store_type: str = Field(
        default="in-memory",
        description="Tipo de store vectorial",
    )
    embedding_model: str = Field(
        default="amazon.titan-embed-text-v1",
        description="Modelo de embeddings",
    )
    embedding_dimension: int = Field(
        default=1536,
        description="Dimensión de los embeddings",
    )
    
    cors_origins: list[str] = Field(
        default=["*"],
        description="Orígenes permitidos para CORS",
    )
    
    cache_ttl: int = Field(
        default=3600,
        description="TTL de cache en segundos",
    )
    retry_max_attempts: int = Field(
        default=3,
        description="Máximo de reintentos",
    )
    retry_delay: float = Field(
        default=1.0,
        description="Delay entre reintentos en segundos",
    )
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache
def get_settings() -> Settings:
    """
    Obtiene la configuración del sistema.
    
    Utiliza lru_cache para evitar recrear la configuración en cada llamada.
    """
    return Settings()


def get_aws_credentials() -> dict:
    """
    Obtiene las credenciales de AWS desde variables de entorno.
    
    Returns:
        Diccionario con access_key y secret_key
    """
    settings = get_settings()
    return {
        "aws_access_key_id": os.getenv("AWS_ACCESS_KEY_ID"),
        "aws_secret_access_key": os.getenv("AWS_SECRET_ACCESS_KEY"),
        "region_name": settings.aws_region,
    }