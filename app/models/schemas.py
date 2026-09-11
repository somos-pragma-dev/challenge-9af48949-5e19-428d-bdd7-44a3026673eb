from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class NormativeQueryRequest(BaseModel):
    """Esquema para solicitudes de consulta normativa."""
    
    query: str = Field(
        ...,
        min_length=1,
        max_length=2000,
        description="Texto de la consulta del usuario",
        examples=["¿Cuál es la política de protección de datos?"]
    )
    max_documents: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Número máximo de documentos a recuperar",
    )
    response_format: str = Field(
        default="text",
        description="Formato de respuesta: text o structured",
    )
    language: Optional[str] = Field(
        default="es",
        description="Idioma de la respuesta",
    )
    
    @field_validator("query")
    @classmethod
    def query_not_empty(cls, v: str) -> str:
        """Valida que la consulta no esté vacía después de strip."""
        if not v.strip():
            raise ValueError("La consulta no puede estar vacía")
        return v.strip()
    
    @field_validator("response_format")
    @classmethod
    def validate_format(cls, v: str) -> str:
        """Valida que el formato de respuesta sea válido."""
        allowed = ["text", "structured", "markdown"]
        if v.lower() not in allowed:
            raise ValueError(f"Formato debe ser uno de: {allowed}")
        return v.lower()
    
    class Config:
        json_schema_extra = {
            "example": {
                "query": "¿Cuáles son los procedimientos de venta para clientes corporativos?",
                "max_documents": 5,
                "response_format": "text",
                "language": "es",
            }
        }


class Source(BaseModel):
    """Esquema para una fuente de información."""
    
    id: int = Field(..., description="Identificador de la fuente")
    content: str = Field(..., max_length=500, description="Contenido truncado de la fuente")
    title: Optional[str] = Field(None, description="Título del documento fuente")
    relevance_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Puntuación de relevancia",
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "content": "POLÍTICA DE PROTECCIÓN DE DATOS\n1. ÁMBITO DE APLICACIÓN\nEsta política aplica...",
                "title": "politica_proteccion_datos",
                "relevance_score": 0.95,
            }
        }


class NormativeQueryResponse(BaseModel):
    """Esquema para respuestas de consulta normativa."""
    
    answer: str = Field(..., description="Respuesta generada por el modelo")
    sources: list[Source] = Field(default_factory=list, description="Fuentes utilizadas")
    confidence: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Nivel de confianza de la respuesta",
    )
    metadata: dict[str, Any] = Field(
        default_factory=dict,
        description="Metadatos adicionales de la respuesta",
    )
    
    @field_validator("confidence")
    @classmethod
    def validate_confidence(cls, v: float) -> float:
        """Valida que la confianza esté en el rango correcto."""
        if v < 0.0 or v > 1.0:
            raise ValueError("La confianza debe estar entre 0.0 y 1.0")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "answer": "La política de protección de datos aplica a todos los empleados...",
                "sources": [
                    {
                        "id": 1,
                        "content": "POLÍTICA DE PROTECCIÓN DE DATOS\n1. ÁMBITO...",
                        "title": "politica_proteccion_datos",
                        "relevance_score": 0.95,
                    }
                ],
                "confidence": 0.85,
                "metadata": {
                    "query": "¿Cuál es la política de protección de datos?",
                    "documents_found": 3,
                    "max_response_tokens": 2048,
                },
            }
        }


class HealthCheckResponse(BaseModel):
    """Esquema para respuestas de verificación de estado."""
    
    status: str = Field(..., description="Estado del servicio")
    version: str = Field(..., description="Versión de la aplicación")
    service: str = Field(..., description="Nombre del servicio")
    timestamp: Optional[str] = Field(None, description="Timestamp de la verificación")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "ok",
                "version": "0.1.0",
                "service": "normative-rag-system",
                "timestamp": "2024-01-15T10:30:00Z",
            }
        }


class SystemStatus(BaseModel):
    """Esquema para el estado general del sistema."""
    
    status: str = Field(..., description="Estado general del sistema")
    repository_connected: bool = Field(..., description="Conexión al repositorio")
    model_loaded: bool = Field(..., description="Modelo cargado")
    active_connections: int = Field(..., ge=0, description="Conexiones activas")
    uptime_seconds: Optional[int] = Field(None, description="Tiempo de actividad en segundos")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "operational",
                "repository_connected": True,
                "model_loaded": True,
                "active_connections": 5,
                "uptime_seconds": 3600,
            }
        }


class ErrorResponse(BaseModel):
    """Esquema para respuestas de error."""
    
    detail: str = Field(..., description="Descripción del error")
    type: Optional[str] = Field(None, description="Tipo de error")
    code: Optional[str] = Field(None, description="Código de error")
    
    class Config:
        json_schema_extra = {
            "example": {
                "detail": "Error al procesar la consulta",
                "type": "ValidationError",
                "code": "QUERY_001",
            }
        }