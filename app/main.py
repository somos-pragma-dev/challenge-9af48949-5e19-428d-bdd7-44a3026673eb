import logging
import os
from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config.settings import Settings, get_settings
from app.models.schemas import (
    NormativeQueryRequest,
    NormativeQueryResponse,
    HealthCheckResponse,
    SystemStatus,
)
from app.retrieval.normative_repository import NormativeRepository

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """Inicializa los recursos del sistema al arrancar la aplicación."""
    settings = get_settings()
    logger.info("Inicializando sistema de respuestas normativas...")
    
    try:
        repository = NormativeRepository(settings)
        await repository.initialize()
        app.state.repository = repository
        logger.info("Repositorio de normativas inicializado correctamente")
    except Exception as e:
        logger.error(f"Error al inicializar el repositorio: {e}")
        raise
    
    yield
    
    logger.info("Cerrando recursos del sistema...")
    if hasattr(app.state, "repository"):
        await app.state.repository.close()


def create_app(settings: Settings | None = None) -> FastAPI:
    """Crea y configura la aplicación FastAPI."""
    if settings is None:
        settings = get_settings()
    
    app = FastAPI(
        title="Sistema de Respuestas Normativas",
        description="API para consultas sobre normativa interna utilizando modelos generativos",
        version="0.1.0",
        docs_url="/docs" if settings.debug else None,
        redoc_url="/redoc" if settings.debug else None,
        lifespan=lifespan,
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    @app.get("/", response_model=HealthCheckResponse)
    async def root() -> HealthCheckResponse:
        """Endpoint de verificación de estado del sistema."""
        return HealthCheckResponse(
            status="ok",
            version="0.1.0",
            service="normative-rag-system",
        )
    
    @app.get("/health", response_model=HealthCheckResponse)
    async def health_check() -> HealthCheckResponse:
        """Endpoint de verificación de salud de la aplicación."""
        return HealthCheckResponse(
            status="ok",
            version="0.1.0",
            service="normative-rag-system",
        )
    
    @app.get("/status", response_model=SystemStatus)
    async def system_status() -> SystemStatus:
        """Obtiene el estado general del sistema incluyendo métricas."""
        return SystemStatus(
            status="operational",
            repository_connected=True,
            model_loaded=True,
            active_connections=0,
        )
    
    @app.post(
        "/api/v1/query",
        response_model=NormativeQueryResponse,
        status_code=status.HTTP_200_OK,
    )
    async def query_normative(
        request: NormativeQueryRequest,
    ) -> NormativeQueryResponse:
        """
        Procesa una consulta normativa y devuelve una respuesta estructurada.
        
        El sistema recupera contexto relevante del repositorio de normativas,
        genera una respuesta utilizando el modelo generativo y la estructura
        según el esquema de respuesta definido.
        """
        if not hasattr(app.state, "repository"):
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Sistema no inicializado correctamente",
            )
        
        repository: NormativeRepository = app.state.repository
        
        try:
            logger.info(f"Procesando consulta: {request.query[:100]}...")
            
            context_docs = await repository.retrieve_relevant_documents(
                query=request.query,
                max_documents=request.max_documents,
            )
            
            if not context_docs:
                logger.warning("No se encontró contexto relevante para la consulta")
                return NormativeQueryResponse(
                    answer="No se encontró información relevante para responder a su consulta en el repositorio de normativas.",
                    sources=[],
                    confidence=0.0,
                    metadata={"query": request.query, "documents_found": 0},
                )
            
            context_text = "\n\n".join(
                f"[Documento {i+1}]: {doc}" 
                for i, doc in enumerate(context_docs)
            )
            
            answer = await repository.generate_response(
                query=request.query,
                context=context_text,
                response_format=request.response_format,
            )
            
            sources = [
                {"id": i + 1, "content": doc[:200] + "..."}
                for i, doc in enumerate(context_docs[:3])
            ]
            
            logger.info(f"Consulta procesada exitosamente")
            
            return NormativeQueryResponse(
                answer=answer,
                sources=sources,
                confidence=0.85,
                metadata={
                    "query": request.query,
                    "documents_found": len(context_docs),
                    "max_response_tokens": settings.max_response_tokens,
                },
            )
            
        except Exception as e:
            logger.error(f"Error al procesar consulta: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar la consulta: {str(e)}",
            )
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Any, exc: Exception) -> JSONResponse:
        """Manejador global de excepciones no controladas."""
        logger.error(f"Excepción no controlada: {exc}", exc_info=True)
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "detail": "Error interno del servidor",
                "type": type(exc).__name__,
            },
        )
    
    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn
    settings = get_settings()
    uvicorn.run(
        "app.main:app",
        host=settings.host,
        port=settings.port,
        reload=settings.debug,
        log_level=settings.log_level.lower(),
    )