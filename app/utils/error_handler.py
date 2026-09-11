"""Manejador global de errores para gestionar fallos en la recuperación de contexto,
generación de respuestas y evaluación."""

import logging
import traceback
from enum import Enum
from typing import Any, Callable, TypeVar

from botocore.exceptions import ClientError, BotoCoreError
from fastapi import Request
from fastapi.responses import JSONResponse
from langchain_core.messages import HumanMessage, AIMessage
from pydantic import BaseModel

from app.config.settings import get_settings, Settings
from app.models.schemas import ErrorResponse

logger = logging.getLogger(__name__)

T = TypeVar("T")


class ErrorCode(str, Enum):
    """Códigos de error del sistema."""

    RETRIEVAL_ERROR = "RETRIEVAL_ERROR"
    GENERATION_ERROR = "GENERATION_ERROR"
    EVALUATION_ERROR = "EVALUATION_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    CONFIGURATION_ERROR = "CONFIGURATION_ERROR"
    TIMEOUT_ERROR = "TIMEOUT_ERROR"
    UNKNOWN_ERROR = "UNKNOWN_ERROR"


class ErrorSeverity(str, Enum):
    """Nivel de severidad del error."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class ErrorContext(BaseModel):
    """Contexto de un error ocurrido en el sistema."""

    error_code: ErrorCode
    severity: ErrorSeverity
    message: str
    details: dict[str, Any] | None = None
    recoverable: bool = True


class RecoveryStrategy(str, Enum):
    """Estrategias de recuperación disponibles."""

    RETRY = "retry"
    FALLBACK = "fallback"
    GRACEFUL_DEGRADATION = "graceful_degradation"
    FAIL = "fail"


class ErrorHandler:
    """Manejador centralizado de errores del sistema."""

    def __init__(self, settings: Settings | None = None):
        self.settings = settings or get_settings()
        self._error_log: list[ErrorContext] = []
        self._max_log_size = 100

    def log_error(self, context: ErrorContext) -> None:
        """Registra un error en el log del manejador."""
        self._error_log.append(context)
        if len(self._error_log) > self._max_log_size:
            self._error_log = self._error_log[-self._max_log_size :]

        log_level = {
            ErrorSeverity.LOW: logging.WARNING,
            ErrorSeverity.MEDIUM: logging.ERROR,
            ErrorSeverity.HIGH: logging.ERROR,
            ErrorSeverity.CRITICAL: logging.CRITICAL,
        }.get(context.severity, logging.ERROR)

        logger.log(
            log_level,
            f"[{context.error_code}] {context.message}",
            extra={"details": context.details},
        )

    def get_recovery_strategy(self, error_code: ErrorCode) -> RecoveryStrategy:
        """Determina la estrategia de recuperación según el tipo de error."""
        strategies = {
            ErrorCode.RETRIEVAL_ERROR: RecoveryStrategy.FALLBACK,
            ErrorCode.GENERATION_ERROR: RecoveryStrategy.RETRY,
            ErrorCode.EVALUATION_ERROR: RecoveryStrategy.GRACEFUL_DEGRADATION,
            ErrorCode.VALIDATION_ERROR: RecoveryStrategy.FAIL,
            ErrorCode.CONFIGURATION_ERROR: RecoveryStrategy.FAIL,
            ErrorCode.TIMEOUT_ERROR: RecoveryStrategy.RETRY,
            ErrorCode.UNKNOWN_ERROR: RecoveryStrategy.GRACEFUL_DEGRADATION,
        }
        return strategies.get(error_code, RecoveryStrategy.FAIL)

    def create_error_response(
        self,
        error_code: ErrorCode,
        message: str,
        details: dict[str, Any] | None = None,
    ) -> ErrorResponse:
        """Crea una respuesta de error estructurada."""
        severity = self._determine_severity(error_code)
        context = ErrorContext(
            error_code=error_code,
            severity=severity,
            message=message,
            details=details,
        )
        self.log_error(context)

        return ErrorResponse(
            error=error_code.value,
            message=message,
            details=details,
        )

    def _determine_severity(self, error_code: ErrorCode) -> ErrorSeverity:
        """Determina la severidad del error según su código."""
        severity_map = {
            ErrorCode.RETRIEVAL_ERROR: ErrorSeverity.MEDIUM,
            ErrorCode.GENERATION_ERROR: ErrorSeverity.HIGH,
            ErrorCode.EVALUATION_ERROR: ErrorSeverity.LOW,
            ErrorCode.VALIDATION_ERROR: ErrorSeverity.MEDIUM,
            ErrorCode.CONFIGURATION_ERROR: ErrorSeverity.CRITICAL,
            ErrorCode.TIMEOUT_ERROR: ErrorSeverity.MEDIUM,
            ErrorCode.UNKNOWN_ERROR: ErrorSeverity.HIGH,
        }
        return severity_map.get(error_code, ErrorSeverity.MEDIUM)

    def handle_retrieval_error(
        self,
        query: str,
        exception: Exception,
    ) -> tuple[str | None, ErrorResponse]:
        """Maneja errores en la recuperación de contexto."""
        details = {
            "query": query,
            "exception_type": type(exception).__name__,
            "exception_message": str(exception),
        }

        if isinstance(exception, ClientError):
            details["aws_error_code"] = exception.response.get("Error", {}).get("Code")

        error_response = self.create_error_response(
            ErrorCode.RETRIEVAL_ERROR,
            f"Error al recuperar contexto: {str(exception)}",
            details,
        )

        strategy = self.get_recovery_strategy(ErrorCode.RETRIEVAL_ERROR)
        if strategy == RecoveryStrategy.FALLBACK:
            logger.info("Estrategia de recuperación: fallback a búsqueda local")
            return None, error_response

        return None, error_response

    def handle_generation_error(
        self,
        context: str,
        query: str,
        exception: Exception,
    ) -> tuple[str | None, ErrorResponse]:
        """Maneja errores en la generación de respuestas."""
        details = {
            "query": query,
            "context_length": len(context) if context else 0,
            "exception_type": type(exception).__name__,
            "exception_message": str(exception),
        }

        if isinstance(exception, (ClientError, BotoCoreError)):
            details["recoverable"] = True
        else:
            details["recoverable"] = False

        error_response = self.create_error_response(
            ErrorCode.GENERATION_ERROR,
            f"Error al generar respuesta: {str(exception)}",
            details,
        )

        strategy = self.get_recovery_strategy(ErrorCode.GENERATION_ERROR)
        if strategy == RecoveryStrategy.RETRY:
            logger.info("Estrategia de recuperación: reintento de generación")
            return None, error_response

        return None, error_response

    def handle_evaluation_error(
        self,
        query: str,
        response: str,
        exception: Exception,
    ) -> tuple[dict[str, Any] | None, ErrorResponse]:
        """Maneja errores en la evaluación de respuestas."""
        details = {
            "query": query,
            "response_length": len(response) if response else 0,
            "exception_type": type(exception).__name__,
            "exception_message": str(exception),
        }

        error_response = self.create_error_response(
            ErrorCode.EVALUATION_ERROR,
            f"Error al evaluar respuesta: {str(exception)}",
            details,
        )

        strategy = self.get_recovery_strategy(ErrorCode.EVALUATION_ERROR)
        if strategy == RecoveryStrategy.GRACEFUL_DEGRADATION:
            logger.info("Estrategia de recuperación: degradación graceful en evaluación")
            return {"confidence": 0.0, "metrics": {}}, error_response

        return None, error_response


async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Manejador global de excepciones para FastAPI."""
    error_handler = ErrorHandler()

    tb_str = "".join(traceback.format_exception(type(exc), exc, exc.__traceback__))

    error_response = error_handler.create_error_response(
        ErrorCode.UNKNOWN_ERROR,
        f"Error interno del servidor: {str(exc)}",
        {
            "path": str(request.url),
            "method": request.method,
            "exception_type": type(exc).__name__,
            "traceback": tb_str,
        },
    )

    return JSONResponse(
        status_code=500,
        content=error_response.model_dump(),
    )


def with_error_handling(
    error_code: ErrorCode,
    fallback_value: T | None = None,
):
    """Decorador para manejo de errores en funciones síncronas.

    Args:
        error_code: Código de error a usar en caso de excepción.
        fallback_value: Valor a retornar en caso de error recuperable.
    """

    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        def wrapper(*args: Any, **kwargs: Any) -> T:
            error_handler = ErrorHandler()
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error en {func.__name__}: {e}")
                error_response = error_handler.create_error_response(
                    error_code,
                    f"Error en {func.__name__}: {str(e)}",
                    {"function": func.__name__},
                )
                if fallback_value is not None:
                    return fallback_value
                raise

        return wrapper

    return decorator