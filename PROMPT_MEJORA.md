# Prompt para Mejorar el Codigo Base

Copia y pega el contenido del bloque de abajo en un asistente de IA (Claude, ChatGPT)
para obtener un ZIP con el proyecto completo y arrancable.

Si preferis trabajar en tu editor con un agente local (Claude Code, Cursor, Copilot), usa `AGENTS.md` en vez de este archivo: dice lo mismo pero para que escriba los archivos en disco.

## Las dos reglas que no se negocian

1. **Completa el boilerplate.** Todo lo que el proyecto necesita para compilar y arrancar: manifiesto de dependencias, punto de entrada, configuracion, capa de interfaz, y las capas del patron arquitectonico declarado. Eso es andamiaje y es tu trabajo.
2. **NO resuelvas el reto.** Los entregables de las fases son el trabajo de la persona. El hueco pedagogico se deja como esta: el proyecto arranca, pero lo que el reto pide implementar NO esta implementado.

Dicho de otra forma: si algo impide compilar, arreglalo. Si algo es logica de negocio incompleta, validaciones ausentes, un secreto hardcodeado o un patron mejorable, dejalo exactamente como esta — es lo que la persona tiene que encontrar.

## Lo que le falta a este proyecto

Esto NO lo tenes que adivinar: salio de comparar el proyecto contra la arquitectura declarada del reto y de un analisis estatico del codigo. Completalo TODO.

### Archivos que la arquitectura del reto declara y no estan

Creálos con implementacion real, en la capa que les corresponde:

- `app/retrieval/vector_store.py`
- `app/chains/normative_chain.py`

### Referencias colgando en el codigo que si esta

Cada una rompe la compilacion:

- `app/utils/aws_client.py` — `Settings.info`: Se invoca `info` sobre `Settings`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/utils/aws_client.py` — `Settings.debug`: Se invoca `debug` sobre `Settings`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/utils/aws_client.py` — `Settings.error`: Se invoca `error` sobre `Settings`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/utils/aws_client.py` — `Settings.warning`: Se invoca `warning` sobre `Settings`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/utils/error_handler.py` — `ErrorResponse.log`: Se invoca `log` sobre `ErrorResponse`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/utils/error_handler.py` — `ErrorResponse.info`: Se invoca `info` sobre `ErrorResponse`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.
- `app/utils/error_handler.py` — `ErrorResponse.error`: Se invoca `error` sobre `ErrorResponse`, pero esa clase no declara ese metodo. Agregalo con su implementacion real, o usa uno de los que si declara.

## Como saber que terminaste

```bash
pip install -r requirements.txt && pytest -q
```

Ese comando corriendo sin errores es la definicion de "listo".

---

```
## Briefing del reto (autoridad)
Este bloque manda sobre los archivos adjuntos. El stack y el rol salen de AQUÍ, no de un topic genérico ni de markdown placeholder.

### Perfil
Chapter Ciencia de Datos, Especialidad Ingeniero de IA, Tecnología AWS Bedrock, Senior

### Brecha de conocimiento
Construye soluciones sobre modelos generativos con recuperacion de contexto, salida estructurada y evaluacion medible

### Misión / candidato
Responder consultas sobre la normativa interna

### Reto
- Tema: aplicaciones sobre modelos generativos
- Seniority: senior-l2
- Tipo: practical
- Título: Implementación de un sistema de respuestas normativas con modelos generativos
- Tiempo estimado: 2 semanas

### Fases (trabajo del HUMANO — PROHIBIDO completarlas)
No implementes estos entregables. Dejalos como hueco pedagógico. El asistente solo materializa el proyecto arrancable para que el participante pueda trabajar.
- Fase 1: Configuración del entorno y recuperación de contexto — objetivo: Establecer el entorno de trabajo y recuperar contexto relevante para las consultas normativas. — entregable (NO resolver): Entorno configurado y mecanismo de recuperación de contexto funcional.
- Fase 2: Generación de respuestas estructuradas — objetivo: Implementar la generación de respuestas estructuradas utilizando el modelo generativo. — entregable (NO resolver): Mecanismo de generación de respuestas estructuradas funcional.
- Fase 3: Evaluación y optimización del sistema — objetivo: Evaluar la precisión y relevancia de las respuestas generadas y optimizar el sistema. — entregable (NO resolver): Sistema optimizado con evaluación medible de la precisión y relevancia de las respuestas.

Eres un asistente experto en análisis, corrección y generación de archivos de cualquier tipo:
código fuente, documentación, hojas de cálculo, documentos Word, configuraciones, entre otros.
Voy a enviarte una cadena de texto que contiene uno o más archivos. Cada archivo está delimitado por un marcador con el siguiente formato:
// === ARCHIVO: ruta/del/archivo.extension ===
o también puede aparecer como:
## === ARCHIVO: ruta/del/archivo.extension ===
Lo que sigue al marcador puede ser:

El contenido real del archivo (código, texto, YAML, etc.)
Una descripción en lenguaje natural de lo que debe contener el archivo


TU TAREA
PASO 0 — ¿Esto es un proyecto o una carcasa?
Antes de extraer archivos, leé el Briefing (si está) y diagnosticá el adjunto.

Es CARCASA si ocurre CUALQUIERA de estas:
- No hay manifiesto de dependencias del stack del briefing (manifest.json de VTEX IO / package.json / pom.xml / build.gradle / requirements.txt / go.mod / *.tf / *.csproj, según corresponda)
- Hay un "binario" que en realidad es un comentario ("no puede ser mostrado como texto plano", placeholder .fig/.docx vacío)
- Los markdowns ya completan entregables de fases posteriores ("se implementó fade-in", lista de áreas ya resuelta)

Si es CARCASA:
- MATERIALIZÁ un proyecto que arranca en el stack del briefing (VTEX IO Store Framework, Angular, Terraform, pytest, Nest, etc.). Incluí manifiesto, punto de entrada y capa de interfaz reales.
- NO copies los markdowns de "solución" como si fueran el producto. Son ruido de generación.
- NO resuelvas las fases del briefing (están marcadas PROHIBIDO). Dejá el hueco pedagógico: el flujo existe, las microinteracciones/calidad/infra que el reto pide NO están hechas.
- Después seguí al PASO 5 (ZIP).

Si es un proyecto REAL (manifiesto + código que compila o arranca):
- Seguí PASO 1 en adelante. 🔴 compilación sí. 🟡 pedagógico no.

PASO 1 — Detección y extracción
Identifica todos los archivos presentes en la cadena. Para cada archivo extrae:

Su ruta completa (ej: src/main/java/com/pragma/Service.java)
Su contenido o descripción

PASO 2 — Clasificación por tipo
Clasifica cada archivo en una de estas categorías:
A) Código fuente (Java, Python, TypeScript, JavaScript, Kotlin, etc.)
B) Configuración / documentación (YAML, properties, Markdown, JSON, txt, etc.)
C) Excel (.xlsx, .xls, .csv)
D) Word (.docx, .doc)
E) Otro tipo de archivo binario o especial
PASO 3 — Clasificación de errores en código fuente

Objetivo prioritario: que el proyecto compile. No corrijas flujo de negocio ni lógica funcional.

Antes de modificar cualquier archivo de código fuente, clasifica cada problema encontrado en una de estas dos categorías:
🔴 ERROR DE COMPILACIÓN — corregir siempre
Son errores que impiden que el proyecto arranque, sin valor pedagógico:

Import faltante o incorrecto
Clase, método o variable referenciada que no existe en ningún archivo del proyecto
Error de sintaxis
Anotación con atributos inválidos
Dependencia ausente en pom.xml, package.json, etc.
Archivo referenciado que no existe y debe ser creado con implementación mínima

→ CORREGIR estos errores.
🟡 PROBLEMA FUNCIONAL O DE CALIDAD — preservar siempre
Son problemas que no impiden compilar. Pueden ser intencionales para el aprendizaje:

Clave secreta hardcodeada ("secret", "password123")
API deprecada que funciona pero tiene reemplazo moderno
Lógica de negocio incorrecta o incompleta
Código redundante o de baja legibilidad
Falta de validaciones en flujo de negocio
Patrones de diseño incorrectos pero funcionales
Concurrencia no segura
Configuración funcional pero no óptima

→ PRESERVAR tal cual. No corregir, no mejorar, no comentar.
PASO 4 — Procesamiento según tipo de archivo
Tipo A — Código fuente
Aplica únicamente las correcciones clasificadas como 🔴 ERROR DE COMPILACIÓN.
No alteres ningún elemento clasificado como 🟡 PROBLEMA FUNCIONAL O DE CALIDAD.
Si falta un archivo referenciado, créalo con la implementación mínima necesaria para compilar.
Tipo B — Configuración / documentación
Extrae el contenido tal cual, sin modificaciones salvo errores evidentes de sintaxis
(ej: YAML mal indentado).
Tipo C — Excel (.xlsx)
Si viene con contenido real, genera el archivo respetando ese contenido.
Si viene con descripción en lenguaje natural, genera un archivo Excel funcional con:

Fila de encabezados en negrita con color de fondo distintivo
Columnas con ancho ajustado al contenido
Tipos de dato correctos por columna
Validaciones si la descripción lo indica
Hojas nombradas descriptivamente si hay más de una
Filas de ejemplo si no hay datos reales

Tipo D — Word (.docx)
Si viene con contenido real, genera el archivo respetando ese contenido.
Si viene con descripción en lenguaje natural, genera un documento Word funcional con:

Estilos de título (Título 1, Título 2) para jerarquía de secciones
Fuente legible (Calibri o equivalente), tamaño 11-12pt para cuerpo
Márgenes estándar
Tabla de contenido si tiene múltiples secciones
Tablas con encabezados en negrita si aplica

Tipo E — Otro
Genera el archivo con el contenido o estructura más apropiada según la descripción.
PASO 5 — Exportación en ZIP
Empaqueta todos los archivos en un único archivo ZIP descargable respetando exactamente
la estructura de rutas indicada por los marcadores.
El ZIP debe incluir:

Archivos de código con únicamente los errores de compilación corregidos
Archivos de configuración y documentación sin cambios
Archivos nuevos creados para resolver dependencias de compilación faltantes
Archivos Excel y Word generados desde descripción

IMPORTANTE: El ZIP debe estar listo para descargar al finalizar. No preguntes si el usuario
quiere generarlo. Simplemente genera el archivo y proporciona el enlace de descarga; No debes desplegar en el chat el resumen de lo que arreglaste al Zip, solo entregalo.

REGLAS IMPORTANTES

No omitas ningún archivo aunque no tenga errores ni modificaciones
Respeta los nombres y rutas exactas indicadas por los marcadores
Si un archivo no tiene marcador claro, infiere el nombre desde su contenido
Si la cadena contiene solo documentación, placeholders o binarios fake, NO la reproduzcas:
aplicá PASO 0 (materializar el proyecto del briefing). Reproducir la carcasa es un fallo.
No agregues texto después del enlace de descarga del ZIP
No preguntes si el usuario quiere el ZIP: simplemente generalo siempre
Si detectas que falta un archivo de configuración necesario para compilar
(pom.xml, package.json, requirements.txt, build.gradle, etc.), créalo e inclúyelo
inferiendo su contenido desde los imports y frameworks detectados en el código
Nunca corrijas problemas 🟡 aunque parezcan obvios o fáciles de mejorar.
El participante que recibirá este proyecto los debe encontrar y resolver él mismo.


INPUT
Aquí está la cadena con los archivos:

// === ARCHIVO: pyproject.toml ===
[project]
name = "normative-rag-system"
version = "0.1.0"
description = "Sistema de respuestas normativas con modelos generativos"
requires-python = ">=3.13"
dependencies = [
    "fastapi==0.115.0",
    "uvicorn==0.30.1",
    "langchain==0.2.5",
    "langchain-aws==0.1.5",
    "langgraph==0.0.48",
    "pydantic==2.7.1",
    "boto3==1.34.123",
    "numpy==1.26.4",
    "pandas==2.2.2",
    "python-dotenv==1.0.1",
]

[project.optional-dependencies]
test = [
    "pytest==8.2.0",
    "httpx==0.27.0",
]
dev = [
    "pytest==8.2.0",
    "httpx==0.27.0",
    "python-dotenv==1.0.1",
]

[build-system]
requires = ["setuptools>=61.0"]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = "-q --tb=short"

[tool.ruff]
line-length = 120
target-version = "py313"

// === ARCHIVO: app/main.py ===
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

// === ARCHIVO: app/config/settings.py ===
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

// === ARCHIVO: app/retrieval/normative_repository.py ===
import json
import logging
from typing import Any, Optional

import boto3
from botocore.exceptions import ClientError, BotoCoreError

from app.config.settings import Settings, get_settings

logger = logging.getLogger(__name__)


class NormativeRepository:
    """
    Cliente para acceder al repositorio de normativas.
    
    Proporciona métodos para recuperar documentos relevantes,
    cargar normativas para indexación y generar respuestas
    utilizando el modelo generativo.
    """
    
    def __init__(self, settings: Settings | None = None) -> None:
        """Inicializa el repositorio de normativas."""
        self.settings = settings or get_settings()
        self._s3_client: Optional[Any] = None
        self._bedrock_client: Optional[Any] = None
        self._documents_cache: dict[str, list[str]] = {}
        logger.info(f"NormativeRepository inicializado (tipo: {self.settings.normative_repo_type})")
    
    async def initialize(self) -> None:
        """Inicializa los clientes de AWS y carga el índice de documentos."""
        logger.info("Inicializando clientes de AWS...")
        
        self._s3_client = boto3.client(
            "s3",
            region_name=self.settings.aws_region,
        )
        
        self._bedrock_client = boto3.client(
            "bedrock-runtime",
            region_name=self.settings.aws_region,
        )
        
        await self._load_document_index()
        logger.info("Índice de documentos cargado correctamente")
    
    async def _load_document_index(self) -> None:
        """Carga el índice de documentos desde el repositorio configurado."""
        if self.settings.normative_repo_type == "s3" and self.settings.normative_bucket:
            await self._load_from_s3()
        elif self.settings.normative_local_path:
            await self._load_from_local()
        else:
            logger.warning("No se configuró repositorio de normativas, usando datos de ejemplo")
            self._documents_cache = self._get_sample_documents()
    
    async def _load_from_s3(self) -> None:
        """Carga documentos desde S3."""
        try:
            response = self._s3_client.list_objects_v2(
                Bucket=self.settings.normative_bucket,
                Prefix="normativas/",
            )
            
            if "Contents" not in response:
                logger.warning(f"No se encontraron objetos en s3://{self.settings.normative_bucket}/normativas/")
                self._documents_cache = self._get_sample_documents()
                return
            
            for obj in response.get("Contents", []):
                key = obj["Key"]
                if key.endswith(".txt") or key.endswith(".md"):
                    doc_response = self._s3_client.get_object(
                        Bucket=self.settings.normative_bucket,
                        Key=key,
                    )
                    content = doc_response["Body"].read().decode("utf-8")
                    doc_id = key.split("/")[-1].replace(".txt", "").replace(".md", "")
                    self._documents_cache[doc_id] = [content]
                    
        except ClientError as e:
            logger.error(f"Error al cargar desde S3: {e}")
            self._documents_cache = self._get_sample_documents()
        except (BotoCoreError, Exception) as e:
            logger.error(f"Error de conexión S3: {e}")
            self._documents_cache = self._get_sample_documents()
    
    async def _load_from_local(self) -> None:
        """Carga documentos desde sistema de archivos local."""
        import os
        from pathlib import Path
        
        base_path = Path(self.settings.normative_local_path)
        if not base_path.exists():
            logger.warning(f"Ruta local no existe: {base_path}")
            self._documents_cache = self._get_sample_documents()
            return
        
        for file_path in base_path.glob("**/*.txt"):
            try:
                content = file_path.read_text(encoding="utf-8")
                doc_id = file_path.stem
                self._documents_cache[doc_id] = [content]
            except Exception as e:
                logger.error(f"Error al leer {file_path}: {e}")
        
        for file_path in base_path.glob("**/*.md"):
            try:
                content = file_path.read_text(encoding="utf-8")
                doc_id = file_path.stem
                self._documents_cache[doc_id] = [content]
            except Exception as e:
                logger.error(f"Error al leer {file_path}: {e}")
        
        if not self._documents_cache:
            logger.warning("No se encontraron documentos locales")
            self._documents_cache = self._get_sample_documents()
    
    def _get_sample_documents(self) -> dict[str, list[str]]:
        """Proporciona documentos de ejemplo para desarrollo."""
        return {
            "polica_proteccion_datos": [
                "POLÍTICA DE PROTECCIÓN DE DATOS\n\n" +
                "1. ÁMBITO DE APLICACIÓN\n" +
                "Esta política aplica a todos los empleados, contratistas y terceros que procesen datos personales en nombre de la organización.\n\n" +
                "2. DEFINICIONES\n" +
                "- Datos personales: información que identifica a una persona física.\n" +
                "- Tratamiento: cualquier operación sobre datos personales.\n" +
                "- Responsable: la organización que decide el tratamiento.\n\n" +
                "3. PRINCIPIOS DEL TRATAMIENTO\n" +
                "- Licitud, lealtad y transparencia.\n" +
                "- Limitación de la finalidad.\n" +
                "- Minimización de datos.\n" +
                "- Exactitud.\n" +
                "- Limitación del plazo de conservación.\n" +
                "- Integridad y confidencialidad.\n"
            ],
            "codigo_conducta": [
                "CÓDIGO DE CONDUCTA EMPRESARIAL\n\n" +
                "1. MISIÓN Y VALORES\n" +
                "La empresa se compromete a operar con integridad, respeto y excelencia en todas sus operaciones.\n\n" +
                "2. NORMAS DE CONDUCTA\n" +
                "- Integridad: actuar con honestidad en todas las transacciones.\n" +
                "- Respeto: tratar a todos con dignidad y respeto.\n" +
                "- Confidencialidad: proteger la información sensible.\n" +
                "- Cumplimiento: respetar las leyes y regulaciones aplicables.\n\n" +
                "3. CONFLICTOS DE INTERÉS\n" +
                "Los empleados deben evitar situaciones que puedan generar conflicto entre sus intereses personales y los de la empresa."
            ],
            "procedimiento_ventas": [
                "PROCEDIMIENTO DE VENTAS\n\n" +
                "1. OBJETIVO\n" +
                "Establecer el proceso de venta para garantizar consistencia y cumplimiento normativo.\n\n" +
                "2. ETAPAS DEL PROCESO\n" +
                "- Prospección: identificación de clientes potenciales.\n" +
                "- Calificación: evaluación de necesidades y presupuesto.\n" +
                "- Presentación: demostración de productos/servicios.\n" +
                "- Negociación: acuerdo de términos comerciales.\n" +
                "- Cierre: formalización de la venta.\n" +
                "- Seguimiento: post-venta y satisfacción del cliente.\n\n" +
                "3. AUTORIZACIONES\n" +
                "Las ventas superiores a 50,000€ requieren autorización del director de área."
            ],
        }
    
    async def retrieve_relevant_documents(
        self,
        query: str,
        max_documents: int = 5,
    ) -> list[str]:
        """
        Recupera documentos relevantes para una consulta.
        
        Args:
            query: Texto de la consulta del usuario
            max_documents: Número máximo de documentos a recuperar
            
        Returns:
            Lista de documentos relevantes ordenados por similitud
        """
        logger.info(f"Recuperando documentos para query: {query[:50]}...")
        
        query_lower = query.lower()
        query_terms = set(query_lower.split())
        
        scored_docs: list[tuple[str, float]] = []
        
        for doc_id, contents in self._documents_cache.items():
            for content in contents:
                content_lower = content.lower()
                content_terms = set(content_lower.split())
                
                common_terms = query_terms.intersection(content_terms)
                score = len(common_terms) / max(len(query_terms), 1)
                
                for term in ["política", "procedimiento", "normativa", "regla", "ley"]:
                    if term in content_lower:
                        score *= 1.2
                
                scored_docs.append((content, score))
        
        scored_docs.sort(key=lambda x: x[1], reverse=True)
        
        result = [doc for doc, score in scored_docs[:max_documents]]
        logger.info(f"Recuperados {len(result)} documentos relevantes")
        
        return result
    
    async def generate_response(
        self,
        query: str,
        context: str,
        response_format: str = "text",
    ) -> str:
        """
        Genera una respuesta utilizando Bedrock.
        
        Args:
            query: Consulta del usuario
            context: Contexto recuperado del repositorio
            response_format: Formato de respuesta deseado
            
        Returns:
            Respuesta generada por el modelo
        """
        logger.info("Generando respuesta con Bedrock...")
        
        prompt = self._build_prompt(query, context, response_format)
        
        try:
            body = json.dumps({
                "anthropic_version": "bedrock-2023-05-31",
                "max_tokens": self.settings.bedrock_max_tokens,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                "temperature": self.settings.bedrock_temperature,
                "top_p": self.settings.bedrock_top_p,
            })
            
            response = self._bedrock_client.invoke_model(
                modelId=self.settings.bedrock_model_id,
                body=body,
                accept="application/json",
                contentType="application/json",
            )
            
            response_body = json.loads(response["body"].read())
            answer = response_body["content"][0]["text"]
            
            logger.info("Respuesta generada exitosamente")
            return answer
            
        except ClientError as e:
            logger.error(f"Error de Bedrock: {e}")
            return self._generate_fallback_response(query, context)
        except (BotoCoreError, Exception) as e:
            logger.error(f"Error al invocar modelo: {e}")
            return self._generate_fallback_response(query, context)
    
    def _build_prompt(self, query: str, context: str, response_format: str) -> str:
        """Construye el prompt para el modelo."""
        format_instruction = ""
        if response_format == "structured":
            format_instruction = "Responde en formato JSON con los campos: respuesta, fuentes, nivel_confianza."
        
        prompt = f"""Eres un asistente de cumplimiento normativo. Utiliza el siguiente contexto para responder la pregunta del usuario.

Contexto:
{context}

Pregunta: {query}

{format_instruction}

Responde de manera clara, precisa y引用 las fuentes del contexto cuando sea relevante."""
        return prompt
    
    def _generate_fallback_response(self, query: str, context: str) -> str:
        """Genera una respuesta de fallback cuando el modelo no está disponible."""
        return (
            f"Basándome en el contexto disponible:\n\n"
            f"He encontrado información relevante en el repositorio de normativas. "
            f"Sin embargo, en este momento no puedo generar una respuesta completa. "
            f"Por favor, consulte directamente los documentos de políticas y procedimientos."
        )
    
    async def close(self) -> None:
        """Cierra los recursos del cliente."""
        logger.info("Cerrando clientes de AWS...")
        if self._s3_client:
            self._s3_client.close()
        if self._bedrock_client:
            self._bedrock_client.close()

// === ARCHIVO: app/models/schemas.py ===
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


// === ARCHIVO: app/prompts/normative_query_template.txt ===
# Template de Prompt para Consultas Normativas
# Version: 1.0.0
# Descripcion: Plantilla utilizada para generar respuestas estructuradas
#              a partir del contexto recuperado de la base de conocimientos normativa.
# Uso: Este template se utiliza en el pipeline RAG para construir el prompt
#      que se envia al modelo generativo, combinando la consulta del usuario,
#      el contexto recuperado y el formato de respuesta esperado.

Eres un asistente especializado en consultas sobre normativa interna de la organizacion.
Tu tarea es analizar la consulta del usuario y generar una respuesta precisa y estructurada
basandote UNICAMENTE en el contexto proporcionado.

## Contexto Normativo
{context}

## Consulta del Usuario
{query}

## Instrucciones de Respuesta
1. Responde basandote EXCLUSIVAMENTE en la informacion del contexto proporcionado.
2. Si la informacion del contexto no es suficiente para responder, indica claramente
   las limitaciones y sugiere areas donde se requiere informacion adicional.
3. Proporciona referencias especificas a los documentos normativos cuando sea aplicable.
4. Estructura tu respuesta de manera clara y profesional.

## Formato de Respuesta Esperado
{response_format}

## Restricciones
- No inventes informacion que no este presente en el contexto.
- No proporciones opiniones personales o interpretaciones no fundamentadas.
- Mantén un tono profesional y objetivo en todo momento.
- Si detectas ambiguedades en la consulta, solicital clarificacion.

Respuesta:


// === ARCHIVO: app/eval/evaluation_dataset.json ===
{
  "evaluation_dataset": [
    {
      "id": "eval_001",
      "query": "¿Cuál es el plazo máximo para responder a una solicitud de acceso a datos personales según el RGPD?",
      "expected_context": ["El plazo máximo para responder a una solicitud de acceso a datos personales es de un mes desde la recepción de la solicitud.", "Este plazo puede extenderse hasta dos meses adicionales en casos de complejidad o volumen de solicitudes.", "La respuesta debe proporcionarse en un formato legible y accesible."],
      "expected_response_pattern": "plazo.*un mes|30 días|treinta días",
      "category": "rgpd_derechos",
      "keywords": ["plazo", "acceso", "datos personales", "RGPD", "mes"],
      "difficulty": "easy"
    },
    {
      "id": "eval_002",
      "query": "¿Qué medidas de seguridad debo implementar para proteger los datos personales de los clientes?",
      "expected_context": ["Se deben implementar medidas técnicas y organizativas apropiadas para garantizar la seguridad de los datos personales.", "Estas medidas incluyen el cifrado de datos, el control de acceso, la autenticación de dos factores y la formación del personal.", "El responsable del tratamiento debe evaluar los riesgos y aplicar medidas proporcionales."],
      "expected_response_pattern": "medidas técnicas|medidas organizativas|cifrado|control de acceso",
      "category": "rgpd_seguridad",
      "keywords": ["medidas de seguridad", "datos personales", "cifrado", "control de acceso"],
      "difficulty": "medium"
    },
    {
      "id": "eval_003",
      "query": "¿Cuál es el procedimiento para reportar una brecha de seguridad que afecte a datos personales?",
      "expected_context": ["En caso de brecha de seguridad que afecte a datos personales, se debe notificar a la autoridad de protección de datos en un plazo máximo de 72 horas.", "Si la brecha representa un alto riesgo para los derechos de las personas, también debe notificarse a los afectados sin dilación.", "La notificación debe incluir la naturaleza de la brecha, las categorías y número de afectados, y las medidas adoptadas."],
      "expected_response_pattern": "72 horas|setenta y dos horas|notificar a la autoridad|notificar a los afectados",
      "category": "rgpd_brechas",
      "keywords": ["brecha", "seguridad", "notificación", "72 horas", "autoridad de control"],
      "difficulty": "medium"
    },
    {
      "id": "eval_004",
      "query": "¿Puedo tratar datos personales de menores de edad sin consentimiento de sus padres?",
      "expected_context": ["El tratamiento de datos de menores de 16 años requiere el consentimiento de sus padres o tutores legales.", "Los servicios de la sociedad de la información dirigidos a menores deben verificar la edad y obtener el consentimiento parental.", "El responsable debe verificar la edad y la identidad del padre, madre o tutor."],
      "expected_response_pattern": "menores de 16 años|consentimiento parental|padres|tutores",
      "category": "rgpd_menores",
      "keywords": ["menores", "consentimiento", "padres", "tutores", "edad"],
      "difficulty": "easy"
    },
    {
      "id": "eval_005",
      "query": "¿Qué derechos tienen los interesados respecto al tratamiento de sus datos personales?",
      "expected_context": ["Los interesados tienen derecho de acceso, rectificación, supresión, limitación del tratamiento, portabilidad y oposición.", "El derecho de acceso permite obtener información sobre los datos tratados y las finalidades del tratamiento.", "El derecho de supresión permite solicitar la eliminación de datos cuando ya no son necesarios o el consentimiento ha sido retirado."],
      "expected_response_pattern": "derecho de acceso|derecho de rectificación|derecho de supresión|derecho de portabilidad",
      "category": "rgpd_derechos",
      "keywords": ["derechos", "acceso", "rectificación", "supresión", "portabilidad", "oposición"],
      "difficulty": "easy"
    },
    {
      "id": "eval_006",
      "query": "¿Cómo debo realizar una evaluación de impacto en la protección de datos personales?",
      "expected_context": ["La evaluación de impacto en la protección de datos (EIPD) es obligatoria cuando el tratamiento puede generar un alto riesgo para los derechos de los interesados.", "La EIPD debe incluir una descripción del tratamiento, la evaluación de la necesidad y proporcionalidad, los riesgos para los derechos de los interesados y las medidas para mitigarlos.", "Debe realizarse antes de iniciar el tratamiento y consultarse con la autoridad de control cuando los riesgos no puedan mitigarse."],
      "expected_response_pattern": "evaluación de impacto|EIPD|alto riesgo|medidas|autoridad de control",
      "category": "rgpd_evaluacion",
      "keywords": ["evaluación de impacto", "EIPD", "riesgos", "medidas", "autoridad"],
      "difficulty": "hard"
    },
    {
      "id": "eval_007",
      "query": "¿Cuál es la normativa aplicable al tratamiento de datos de salud?",
      "expected_context": ["Los datos de salud son categoría especial de datos personales y requieren protección reforzada.", "Su tratamiento está prohibido salvo excepciones previstas en el artículo 9 del RGPD, como el consentimiento explícito o razones de interés público.", "El tratamiento de datos de salud requiere garantías adicionales como la minimización de datos y la limitación del acceso."],
      "expected_response_pattern": "categoría especial|datos de salud|artículo 9|consentimiento explícito|interés público",
      "category": "rgpd_categorias_especiales",
      "keywords": ["datos de salud", "categoría especial", "consentimiento", "artículo 9"],
      "difficulty": "hard"
    },
    {
      "id": "eval_008",
      "query": "¿Qué información debo proporcionar al interesado en el momento de recogida de datos personales?",
      "expected_context": ["En el momento de recogida de datos, debe informarse al interesado sobre la identidad del responsable, la finalidad del tratamiento, los destinatarios, el plazo de conservación y sus derechos.", "También debe informarse sobre la base jurídica del tratamiento y, en su caso, la intención de transferir datos a terceros países.", "La información debe proporcionarse de forma concisa, transparente, inteligible y de fácil acceso."],
      "expected_response_pattern": "identidad del responsable|finalidad|destinatarios-plazo de conservación|derechos|base jurídica",
      "category": "rgpd_transparencia",
      "keywords": ["información", "responsable", "finalidad", "derechos", "transparencia"],
      "difficulty": "medium"
    },
    {
      "id": "eval_009",
      "query": "¿Cómo puedo transferir datos personales a un país fuera del Espacio Económico Europeo?",
      "expected_context": ["La transferencia de datos a países fuera del EEE requiere garantías adecuadas según el RGPD.", "Estas garantías incluyen decisiones de adecuación, cláusulas contractuales tipo o normas corporativas vinculantes.", "El destinatario debe garantizar un nivel de protección equivalente al europeo."],
      "expected_response_pattern": "transferencia|EEE|decisión de adecuación|cláusulas contractuales tipo|normas corporativas",
      "category": "rgpd_transferencias",
      "keywords": ["transferencia", "EEE", "adecuación", "cláusulas", "tercer país"],
      "difficulty": "hard"
    },
    {
      "id": "eval_010",
      "query": "¿Cuál es el régimen sancionador por incumplimiento del RGPD?",
      "expected_context": ["El RGPD establece sanciones administrativas que pueden alcanzar los 20 millones de euros o el 4% del volumen de negocio anual global.", "Las sanciones se gradúan según la naturaleza de la infracción, el grado de culpabilidad, el beneficio obtenido y las medidas adoptadas.", "Antes de imponer una sanción, la autoridad de control debe dar audiencia al interesado."],
      "expected_response_pattern": "20 millones|4%|volumen de negocio|sanciones administrativas|graduación",
      "category": "rgpd_sanciones",
      "keywords": ["sanciones", "multa", "20 millones", "4%", "infracción"],
      "difficulty": "medium"
    },
    {
      "id": "eval_011",
      "query": "¿Qué es el derecho a la portabilidad de datos personales?",
      "expected_context": ["El derecho a la portabilidad permite al interesado recibir sus datos personales en un formato estructurado y de uso común.", "El interesado puede transmitir esos datos a otro responsable sin que el responsable original lo impida.", "Este derecho aplica cuando el tratamiento se basa en el consentimiento o en un contrato y se realiza por medios automatizados."],
      "expected_response_pattern": "formato estructurado|otro responsable|consentimiento|contrato|medios automatizados",
      "category": "rgpd_derechos",
      "keywords": ["portabilidad", "formato", "transferir", "responsable", "consenti"],
      "difficulty": "medium"
    },
    {
      "id": "eval_012",
      "query": "¿Cuándo puedo tratar datos personales sin el consentimiento del interesado?",
      "expected_context": ["El tratamiento sin consentimiento es posible cuando existe una base jurídica alternativa: ejecución de contrato, obligación legal, interés público o interés legítimo.", "El interés legítimo del responsable puede ser base jurídica si no prevalecen los intereses del interesado.", "Debe documentarse la base jurídica invocada y su análisis de ponderación."],
      "expected_response_pattern": "base jurídica|ejecución de contrato|obligación legal|interés público|interés legítimo",
      "category": "rgpd_base_juridica",
      "keywords": ["consentimiento", "base jurídica", "contrato", "obligación", "interés"],
      "difficulty": "hard"
    },
    {
      "id": "eval_013",
      "query": "¿Qué es un delegdo de protección de datos y cuándo es obligatorio designarlo?",
      "expected_context": ["El Delegado de Protección de Datos (DPD) es una figura que supervisa el cumplimiento de la normativa de protección de datos.", "Su designación es obligatoria en empresas que traten datos a gran escala, traten categorías especiales de datos o realicen perfilado sistemático.", "El DPD debe обладать conocimientos especializados y puede ser empleado o consultor externo."],
      "expected_response_pattern": "DPD|Delegado de Protección de Datos|gran escala|categorías especiales|perfilado",
      "category": "rgpd_dpd",
      "keywords": ["Delegado", "DPD", "protección de datos", "obligatorio", "conocimiento"],
      "difficulty": "medium"
    },
    {
      "id": "eval_014",
      "query": "¿Cuál es la diferencia entre responsable y encargado del tratamiento?",
      "expected_context": ["El responsable del tratamiento es quien decide los fines y medios del tratamiento de datos personales.", "El encargado del tratamiento es quien trata datos por cuenta del responsable siguiendo sus instrucciones.", "La relación entre ambos debe regularse mediante un contrato que especifique las instrucciones, el plazo y las obligaciones de seguridad."],
      "expected_response_pattern": "responsable|encargado|fines|medios|instrucciones|contrato",
      "category": "rgpd_roles",
      "keywords": ["responsable", "encargado", "tratamiento", "instrucciones", "contrato"],
      "difficulty": "easy"
    },
    {
      "id": "eval_015",
      "query": "¿Cómo debo gestionar las solicitudes de ejercicio de derechos de los interesados?",
      "expected_context": ["Las solicitudes de ejercicio de derechos deben responderse en el plazo máximo de un mes desde su recepción.", "El responsable debe verificar la identidad del solicitante antes de atender la solicitud.", "La respuesta debe provided en formato electrónico salvo que el interesado solicite otro formato.", "Si la solicitud es manifestamente infundada o excesiva, puede cobrarse un canon o rechazarse."],
      "expected_response_pattern": "un mes|verificar identidad|formato electrónico|infundada|excesiva",
      "category": "rgpd_derechos",
      "keywords": ["solicitud", "derechos", "plazo", "identidad", "respuesta"],
      "difficulty": "medium"
    }
  ],
  "metadata": {
    "version": "1.0.0",
    "created_date": "2024-01-15",
    "total_cases": 15,
    "categories": [
      "rgpd_derechos",
      "rgpd_seguridad",
      "rgpd_brechas",
      "rgpd_menores",
      "rgpd_evaluacion",
      "rgpd_categorias_especiales",
      "rgpd_transparencia",
      "rgpd_transferencias",
      "rgpd_sanciones",
      "rgpd_base_juridica",
      "rgpd_dpd",
      "rgpd_roles"
    ],
    "difficulty_distribution": {
      "easy": 4,
      "medium": 7,
      "hard": 4
    }
  }
}
// === ARCHIVO: app/eval/metrics.py ===
"""
Métricas de evaluación para el sistema de respuestas normativas.

Implementa métricas para medir precisión, relevancia, consistencia y
calidad general de las respuestas generadas por el sistema RAG.
"""

import json
import re
from pathlib import Path
from typing import Any

import numpy as np


class EvaluationMetrics:
    """Calcula métricas de evaluación para respuestas del sistema RAG."""

    def __init__(self, dataset_path: str | None = None) -> None:
        self.dataset_path = dataset_path
        self.evaluation_cases: list[dict[str, Any]] = []
        if dataset_path:
            self._load_dataset(dataset_path)

    def _load_dataset(self, path: str) -> None:
        """Carga el conjunto de evaluación desde un archivo JSON."""
        dataset_file = Path(path)
        if not dataset_file.exists():
            raise FileNotFoundError(f"Dataset no encontrado: {path}")

        with open(dataset_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.evaluation_cases = data.get("evaluation_dataset", [])

    def calculate_keyword_precision(
        self,
        response: str,
        expected_keywords: list[str],
    ) -> float:
        """
        Calcula la precisión de palabras clave en la respuesta.

        Args:
            response: Respuesta generada por el sistema.
            expected_keywords: Lista de palabras clave esperadas.

        Returns:
            Porcentaje de palabras clave encontradas en la respuesta.
        """
        if not expected_keywords:
            return 1.0

        response_lower = response.lower()
        found_count = sum(
            1 for kw in expected_keywords if kw.lower() in response_lower
        )
        return found_count / len(expected_keywords)

    def calculate_pattern_match(
        self,
        response: str,
        expected_pattern: str,
    ) -> float:
        """
        Verifica si la respuesta coincide con el patrón esperado.

        Args:
            response: Respuesta generada.
            expected_pattern: Expresión regular del patrón esperado.

        Returns:
            1.0 si hay coincidencia, 0.0 si no.
        """
        try:
            pattern = re.compile(expected_pattern, re.IGNORECASE)
            return 1.0 if pattern.search(response) else 0.0
        except re.error:
            return 0.0

    def calculate_context_relevance(
        self,
        retrieved_context: list[str],
        expected_context: list[str],
    ) -> float:
        """
        Calcula la relevancia del contexto recuperado vs esperado.

        Usa similitud de Jaccard entre los conjuntos de oraciones
        más similares del contexto.

        Args:
            retrieved_context: Lista de fragmentos de contexto recuperados.
            expected_context: Lista de fragmentos de contexto esperados.

        Returns:
            Puntuación de relevancia entre 0 y 1.
        """
        if not expected_context or not retrieved_context:
            return 0.0

        def tokenize(text: str) -> set[str]:
            return set(re.findall(r"\b\w+\b", text.lower()))

        def jaccard_similarity(set1: set[str], set2: set[str]) -> float:
            if not set1 or not set2:
                return 0.0
            intersection = len(set1 & set2)
            union = len(set1 | set2)
            return intersection / union if union > 0 else 0.0

        similarities = []
        for exp_ctx in expected_context:
            tokens_exp = tokenize(exp_ctx)
            max_sim = 0.0
            for ret_ctx in retrieved_context:
                tokens_ret = tokenize(ret_ctx)
                sim = jaccard_similarity(tokens_exp, tokens_ret)
                max_sim = max(max_sim, sim)
            similarities.append(max_sim)

        return float(np.mean(similarities))

    def calculate_retrieval_precision_at_k(
        self,
        retrieved_docs: list[str],
        expected_docs: list[str],
        k: int = 3,
    ) -> float:
        """
        Calcula Precision@k para el sistema de recuperación.

        Args:
            retrieved_docs: Documentos recuperados ordenados por relevancia.
            expected_docs: Documentos que deberían haber sido recuperados.
            k: Número de documentos a considerar.

        Returns:
            Precision@k como valor entre 0 y 1.
        """
        if k <= 0 or not retrieved_docs:
            return 0.0

        retrieved_k = retrieved_docs[:k]
        relevant_retrieved = sum(
            1 for rdoc in retrieved_k
            if any(self._is_relevant(rdoc, edoc) for edoc in expected_docs)
        )

        return relevant_retrieved / k

    def _is_relevant(self, doc1: str, doc2: str) -> bool:
        """
        Determina si dos documentos son relevantes entre sí.

        Usa tokenización básica y umbral de similitud.
        """
        def get_tokens(text: str) -> set[str]:
            return set(re.findall(r"\b\w+\b", text.lower()))

        tokens1 = get_tokens(doc1)
        tokens2 = get_tokens(doc2)

        if not tokens1 or not tokens2:
            return False

        intersection = len(tokens1 & tokens2)
        min_len = min(len(tokens1), len(tokens2))

        return intersection / min_len >= 0.3

    def calculate_response_consistency(
        self,
        responses: list[str],
    ) -> float:
        """
        Calcula la consistencia entre múltiples respuestas a consultas similares.

        Args:
            responses: Lista de respuestas a evaluar.

        Returns:
            Puntuación de consistencia (1.0 = perfectamente consistente).
        """
        if len(responses) < 2:
            return 1.0

        def get_tokens(text: str) -> set[str]:
            return set(re.findall(r"\b\w+\b", text.lower()))

        token_sets = [get_tokens(resp) for resp in responses]
        consistencies = []

        for i in range(len(token_sets)):
            for j in range(i + 1, len(token_sets)):
                set1, set2 = token_sets[i], token_sets[j]
                if not set1 or not set2:
                    continue

                intersection = len(set1 & set2)
                max_len = max(len(set1), len(set2))
                similarity = intersection / max_len if max_len > 0 else 0.0
                consistencies.append(similarity)

        return float(np.mean(consistencies)) if consistencies else 0.0

    def calculate_answer_completeness(
        self,
        response: str,
        expected_elements: list[str],
    ) -> float:
        """
        Calcula qué tan completa es la respuesta respecto a elementos esperados.

        Args:
            response: Respuesta generada.
            expected_elements: Elementos que deberían estar presentes.

        Returns:
            Puntuación de completitud entre 0 y 1.
        """
        if not expected_elements:
            return 1.0

        response_lower = response.lower()
        found_elements = sum(
            1 for elem in expected_elements
            if elem.lower() in response_lower
        )

        return found_elements / len(expected_elements)

    def evaluate_single_case(
        self,
        case: dict[str, Any],
        generated_response: str,
        retrieved_context: list[str],
    ) -> dict[str, float]:
        """
        Evalúa un caso individual del conjunto de evaluación.

        Args:
            case: Caso de evaluación con query, expected_context, etc.
            generated_response: Respuesta generada por el sistema.
            retrieved_context: Contexto recuperado por el sistema.

        Returns:
            Diccionario con las métricas calculadas.
        """
        keyword_precision = self.calculate_keyword_precision(
            generated_response,
            case.get("keywords", []),
        )

        pattern_match = self.calculate_pattern_match(
            generated_response,
            case.get("expected_response_pattern", ".*"),
        )

        context_relevance = self.calculate_context_relevance(
            retrieved_context,
            case.get("expected_context", []),
        )

        retrieval_precision = self.calculate_retrieval_precision_at_k(
            retrieved_context,
            case.get("expected_context", []),
            k=3,
        )

        completeness = self.calculate_answer_completeness(
            generated_response,
            case.get("keywords", []),
        )

        return {
            "keyword_precision": keyword_precision,
            "pattern_match": pattern_match,
            "context_relevance": context_relevance,
            "retrieval_precision": retrieval_precision,
            "answer_completeness": completeness,
        }

    def evaluate_dataset(
        self,
        generated_responses: dict[str, tuple[str, list[str]]],
    ) -> dict[str, Any]:
        """
        Evalúa todo el conjunto de datos de evaluación.

        Args:
            generated_responses: Diccionario {case_id: (response, context)}

        Returns:
            Métricas agregadas para todo el dataset.
        """
        if not self.evaluation_cases:
            raise ValueError("No hay casos de evaluación cargados")

        case_results = []

        for case in self.evaluation_cases:
            case_id = case.get("id")
            if case_id not in generated_responses:
                continue

            response, context = generated_responses[case_id]
            result = self.evaluate_single_case(case, response, context)
            result["case_id"] = case_id
            result["category"] = case.get("category", "unknown")
            result["difficulty"] = case.get("difficulty", "unknown")
            case_results.append(result)

        if not case_results:
            return {"error": "No se evaluaron casos"}

        case_results_np = np.array([
            [r["keyword_precision"], r["pattern_match"],
             r["context_relevance"], r["retrieval_precision"],
             r["answer_completeness"]]
            for r in case_results
        ])

        return {
            "total_cases_evaluated": len(case_results),
            "aggregated_metrics": {
                "keyword_precision_mean": float(np.mean(case_results_np[:, 0])),
                "keyword_precision_std": float(np.std(case_results_np[:, 0])),
                "pattern_match_mean": float(np.mean(case_results_np[:, 1])),
                "pattern_match_std": float(np.std(case_results_np[:, 1])),
                "context_relevance_mean": float(np.mean(case_results_np[:, 2])),
                "context_relevance_std": float(np.std(case_results_np[:, 2])),
                "retrieval_precision_mean": float(np.mean(case_results_np[:, 3])),
                "retrieval_precision_std": float(np.std(case_results_np[:, 3])),
                "answer_completeness_mean": float(np.mean(case_results_np[:, 4])),
                "answer_completeness_std": float(np.std(case_results_np[:, 4])),
            },
            "overall_score": float(np.mean(case_results_np)),
            "per_category": self._aggregate_by_category(case_results),
            "per_difficulty": self._aggregate_by_difficulty(case_results),
            "individual_results": case_results,
        }

    def _aggregate_by_category(
        self,
        results: list[dict[str, float]],
    ) -> dict[str, dict[str, float]]:
        """Agrupa resultados por categoría de evaluación."""
        categories: dict[str, list[dict[str, float]]] = {}

        for result in results:
            cat = result.get("category", "unknown")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)

        aggregated = {}
        for cat, cat_results in categories.items():
            scores = np.array([
                [r["keyword_precision"], r["pattern_match"],
                 r["context_relevance"], r["retrieval_precision"],
                 r["answer_completeness"]]
                for r in cat_results
            ])
            aggregated[cat] = {
                "count": len(cat_results),
                "mean_score": float(np.mean(scores)),
                "keyword_precision": float(np.mean(scores[:, 0])),
                "pattern_match": float(np.mean(scores[:, 1])),
                "context_relevance": float(np.mean(scores[:, 2])),
            }

        return aggregated

    def _aggregate_by_difficulty(
        self,
        results: list[dict[str, float]],
    ) -> dict[str, dict[str, float]]:
        """Agrupa resultados por nivel de dificultad."""
        difficulties: dict[str, list[dict[str, float]]] = {}

        for result in results:
            diff = result.get("difficulty", "unknown")
            if diff not in difficulties:
                difficulties[diff] = []
            difficulties[diff].append(result)

        aggregated = {}
        for diff, diff_results in difficulties.items():
            scores = np.array([
                [r["keyword_precision"], r["pattern_match"],
                 r["context_relevance"], r["retrieval_precision"],
                 r["answer_completeness"]]
                for r in diff_results
            ])
            aggregated[diff] = {
                "count": len(diff_results),
                "mean_score": float(np.mean(scores)),
                "keyword_precision": float(np.mean(scores[:, 0])),
                "pattern_match": float(np.mean(scores[:, 1])),
                "context_relevance": float(np.mean(scores[:, 2])),
            }

        return aggregated


def load_default_dataset() -> EvaluationMetrics:
    """Carga el dataset de evaluación por defecto."""
    default_path = Path(__file__).parent / "evaluation_dataset.json"
    return EvaluationMetrics(str(default_path))


// === ARCHIVO: app/utils/aws_client.py ===
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


// === ARCHIVO: app/utils/error_handler.py ===
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


// === ARCHIVO: tests/test_retrieval.py ===
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Any

from app.retrieval.normative_repository import NormativeRepository
from app.config.settings import Settings


class TestNormativeRepository:
    """Pruebas para el módulo de recuperación de contexto y búsqueda vectorial."""

    @pytest.fixture
    def mock_settings(self) -> Settings:
        settings = MagicMock(spec=Settings)
        settings.aws_region = "us-east-1"
        settings.bedrock_model_id = "anthropic.claude-3-sonnet-06202025"
        settings.vector_store_path = "/tmp/vector_store"
        settings.s3_bucket = "test-bucket"
        settings.s3_key = "normatives/index"
        settings.max_tokens = 2048
        settings.temperature = 0.7
        settings.top_k = 5
        settings.enable_rag = True
        return settings

    @pytest.fixture
    def repository(self, mock_settings: Settings) -> NormativeRepository:
        return NormativeRepository(settings=mock_settings)

    @pytest.mark.asyncio
    async def test_initialize_creates_vector_store(self, repository: NormativeRepository) -> None:
        """Verifica que initialize carga el índice vectorial correctamente."""
        with patch.object(repository, "_load_document_index", new_callable=AsyncMock) as mock_load:
            await repository.initialize()
            mock_load.assert_called_once()

    @pytest.mark.asyncio
    async def test_retrieve_relevant_documents_returns_list(self, repository: NormativeRepository) -> None:
        """Verifica que retrieve_relevant_documents retorna una lista de documentos."""
        with patch.object(repository, "_load_document_index", new_callable=AsyncMock):
            await repository.initialize()
        repository.vector_store = MagicMock()
        mock_results = [
            {"content": "Artículo 1: Norma de cumplimiento", "score": 0.95},
            {"content": "Artículo 2: Regulación interna", "score": 0.87},
        ]
        repository.vector_store.similarity_search = MagicMock(return_value=mock_results)

        result = await repository.retrieve_relevant_documents("consulta sobre cumplimiento", top_k=5)

        assert isinstance(result, list)
        assert len(result) == 2
        assert "content" in result[0]
        assert "score" in result[0]

    @pytest.mark.asyncio
    async def test_retrieve_relevant_documents_uses_top_k(self, repository: NormativeRepository) -> None:
        """Verifica que el parámetro top_k limita la cantidad de documentos devueltos."""
        with patch.object(repository, "_load_document_index", new_callable=AsyncMock):
            await repository.initialize()
        repository.vector_store = MagicMock()
        mock_results = [
            {"content": f"Documento {i}", "score": 1.0 - i * 0.1}
            for i in range(10)
        ]
        repository.vector_store.similarity_search = MagicMock(return_value=mock_results)

        result = await repository.retrieve_relevant_documents("test query", top_k=3)

        repository.vector_store.similarity_search.assert_called_once_with("test query", k=3)
        assert len(result) == 3

    @pytest.mark.asyncio
    async def test_retrieve_relevant_documents_empty_query(self, repository: NormativeRepository) -> None:
        """Verifica el comportamiento con query vacía."""
        with patch.object(repository, "_load_document_index", new_callable=AsyncMock):
            await repository.initialize()
        repository.vector_store = MagicMock()

        with pytest.raises(ValueError, match="La consulta no puede estar vacía"):
            await repository.retrieve_relevant_documents("")

    @pytest.mark.asyncio
    async def test_retrieve_relevant_documents_fallback_on_error(self, repository: NormativeRepository) -> None:
        """Verifica que ante error en búsqueda vectorial se retorna contexto alternativo."""
        with patch.object(repository, "_load_document_index", new_callable=AsyncMock):
            await repository.initialize()
        repository.vector_store = MagicMock()
        repository.vector_store.similarity_search = MagicMock(side_effect=Exception("Vector store error"))

        result = await repository.retrieve_relevant_documents("consulta", top_k=5)

        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_generate_response_with_format(self, repository: NormativeRepository) -> None:
        """Verifica que generate_response produce respuesta estructurada."""
        with patch.object(repository, "_load_document_index", new_callable=AsyncMock):
            await repository.initialize()
        with patch("app.retrieval.normative_repository.bedrock_runtime") as mock_bedrock:
            mock_client = MagicMock()
            mock_bedrock.Client.return_value = mock_client
            mock_client.converse.return_value = {
                "output": {"message": {"content": [{"text": "Respuesta estructurada"}]}},
                "usage": {"inputTokens": 100, "outputTokens": 50}
            }
            repository._bedrock_runtime = mock_bedrock.Client.return_value

            context = "Contexto de normativa"
            response = await repository.generate_response(
                "¿Cuáles son las normas de cumplimiento?",
                context,
                response_format="json"
            )

            assert response is not None
            assert "usage" in response or "response" in response

    def test_build_prompt_includes_query_and_context(self, repository: NormativeRepository) -> None:
        """Verifica que el prompt construido incluye query y context."""
        prompt = repository._build_prompt(
            query="¿Qué dice la normativa sobre protección de datos?",
            context="Artículo 5: Protección de datos personales...",
            response_format="json"
        )

        assert "¿Qué dice la normativa sobre protección de datos?" in prompt
        assert "Artículo 5: Protección de datos personales" in prompt
        assert "json" in prompt.lower()

    def test_build_prompt_with_different_formats(self, repository: NormativeRepository) -> None:
        """Verifica que el prompt se adapta al formato de respuesta solicitado."""
        prompt_json = repository._build_prompt("test", "context", "json")
        prompt_text = repository._build_prompt("test", "context", "text")

        assert "json" in prompt_json.lower()
        assert prompt_json != prompt_text

    @pytest.mark.asyncio
    async def test_close_cleans_resources(self, repository: NormativeRepository) -> None:
        """Verifica que close libera los recursos correctamente."""
        repository.vector_store = MagicMock()
        await repository.close()
        assert repository.vector_store is None


class TestNormativeRepositoryIntegration:
    """Pruebas de integración para el repositorio normativo."""

    @pytest.mark.asyncio
    async def test_full_retrieval_flow(self) -> None:
        """Verifica el flujo completo de recuperación: initialize -> retrieve -> generate."""
        with patch("app.retrieval.normative_repository.bedrock_runtime"):
            settings = MagicMock(spec=Settings)
            settings.aws_region = "us-east-1"
            settings.bedrock_model_id = "anthropic.claude-3-sonnet-06202025"
            settings.vector_store_path = "/tmp/test"
            settings.s3_bucket = None
            settings.s3_key = None
            settings.max_tokens = 2048
            settings.temperature = 0.7
            settings.top_k = 5
            settings.enable_rag = True

            repo = NormativeRepository(settings=settings)
            with patch.object(repo, "_load_document_index", new_callable=AsyncMock):
                await repo.initialize()

            repo.vector_store = MagicMock()
            repo.vector_store.similarity_search = MagicMock(return_value=[
                {"content": "Normativa de cumplimiento RGPD", "score": 0.9}
            ])

            docs = await repo.retrieve_relevant_documents("consulta", top_k=3)
            assert len(docs) > 0

// === ARCHIVO: tests/test_chain.py ===
import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from typing import Any

from app.chains.normative_chain import NormativeChain, ChainInput, ChainOutput
from app.config.settings import Settings
from app.retrieval.normative_repository import NormativeRepository


class TestNormativeChain:
    """Pruebas para la orquestación del pipeline RAG con LangGraph."""

    @pytest.fixture
    def mock_settings(self) -> Settings:
        settings = MagicMock(spec=Settings)
        settings.aws_region = "us-east-1"
        settings.bedrock_model_id = "anthropic.claude-3-sonnet-06202025"
        settings.max_tokens = 2048
        settings.temperature = 0.7
        settings.top_k = 5
        settings.enable_rag = True
        return settings

    @pytest.fixture
    def mock_repository(self) -> NormativeRepository:
        repo = MagicMock(spec=NormativeRepository)
        repo.retrieve_relevant_documents = AsyncMock(return_value=[
            {"content": "Contenido normativo relevante", "score": 0.95, "source": "RGPD"},
            {"content": "Artículo sobre protección de datos", "score": 0.88, "source": "LOPD"},
        ])
        repo.generate_response = AsyncMock(return_value={
            "response": "Respuesta generada por el modelo",
            "usage": {"inputTokens": 150, "outputTokens": 80}
        })
        return repo

    @pytest.fixture
    def chain(self, mock_settings: Settings, mock_repository: NormativeRepository) -> NormativeChain:
        return NormativeChain(settings=mock_settings, repository=mock_repository)

    @pytest.mark.asyncio
    async def test_invoke_retrieval_step(self, chain: NormativeChain) -> None:
        """Verifica que el paso de retrieval recupera documentos relevantes."""
        input_data = ChainInput(query="¿Cuáles son los requisitos de protección de datos?")

        result = await chain.invoke(input_data)

        chain.repository.retrieve_relevant_documents.assert_called_once()
        call_args = chain.repository.retrieve_relevant_documents.call_args
        assert call_args[0][0] == "¿Cuáles son los requisitos de protección de datos?"

    @pytest.mark.asyncio
    async def test_invoke_generation_step(self, chain: NormativeChain) -> None:
        """Verifica que el paso de generación produce respuesta."""
        input_data = ChainInput(query="Consulta normativa")

        result = await chain.invoke(input_data)

        chain.repository.generate_response.assert_called_once()
        assert result.response is not None

    @pytest.mark.asyncio
    async def test_invoke_returns_sources(self, chain: NormativeChain) -> None:
        """Verifica que la respuesta incluye las fuentes recuperadas."""
        input_data = ChainInput(query="Consulta")

        result = await chain.invoke(input_data)

        assert hasattr(result, "sources")
        assert len(result.sources) > 0

    @pytest.mark.asyncio
    async def test_invoke_with_empty_query_raises_error(self, chain: NormativeChain) -> None:
        """Verifica que query vacía genera error de validación."""
        input_data = ChainInput(query="")

        with pytest.raises(ValueError, match="Query no puede estar vacía"):
            await chain.invoke(input_data)

    @pytest.mark.asyncio
    async def test_invoke_handles_retrieval_failure(self, chain: NormativeChain) -> None:
        """Verifica el manejo de errores en recuperación."""
        chain.repository.retrieve_relevant_documents = AsyncMock(
            side_effect=Exception("Error de recuperación")
        )
        input_data = ChainInput(query="Consulta de prueba")

        result = await chain.invoke(input_data)

        assert result.response is not None
        assert "error" in result.response.lower() or result.fallback_used is True

    @pytest.mark.asyncio
    async def test_invoke_handles_generation_failure(self, chain: NormativeChain) -> None:
        """Verifica el manejo de errores en generación."""
        chain.repository.generate_response = AsyncMock(
            side_effect=Exception("Error de generación")
        )
        input_data = ChainInput(query="Consulta de prueba")

        result = await chain.invoke(input_data)

        assert result.response is not None
        assert result.fallback_used is True

    @pytest.mark.asyncio
    async def test_invoke_with_custom_top_k(self, chain: NormativeChain) -> None:
        """Verifica que el parámetro top_k se pasa correctamente."""
        input_data = ChainInput(query="Consulta", top_k=10)

        await chain.invoke(input_data)

        call_args = chain.repository.retrieve_relevant_documents.call_args
        assert call_args[1]["top_k"] == 10

    @pytest.mark.asyncio
    async def test_invoke_with_custom_format(self, chain: NormativeChain) -> None:
        """Verifica que el formato de respuesta se pasa a generación."""
        input_data = ChainInput(query="Consulta", response_format="json")

        await chain.invoke(input_data)

        call_args = chain.repository.generate_response.call_args
        assert call_args[0][2] == "json"

    @pytest.mark.asyncio
    async def test_graph_execution_order(self, chain: NormativeChain) -> None:
        """Verifica el orden de ejecución del grafo: retrieval -> generation -> output."""
        input_data = ChainInput(query="Consulta de prueba")

        await chain.invoke(input_data)

        retrieve_call = chain.repository.retrieve_relevant_documents
        generate_call = chain.repository.generate_response

        assert retrieve_call.call_count == 1
        assert generate_call.call_count == 1
        assert retrieve_call.call_count < generate_call.call_count


class TestChainInputOutput:
    """Pruebas para los tipos de entrada y salida de la cadena."""

    def test_chain_input_validation(self) -> None:
        """Verifica la validación del input de la cadena."""
        valid_input = ChainInput(query="Consulta válida")
        assert valid_input.query == "Consulta válida"
        assert valid_input.top_k == 5
        assert valid_input.response_format == "text"

    def test_chain_input_with_custom_params(self) -> None:
        """Verifica input con parámetros personalizados."""
        input_data = ChainInput(
            query="Consulta",
            top_k=10,
            response_format="json"
        )
        assert input_data.top_k == 10
        assert input_data.response_format == "json"

    def test_chain_output_structure(self) -> None:
        """Verifica la estructura del output de la cadena."""
        output = ChainOutput(
            response="Respuesta de prueba",
            sources=["source1", "source2"],
            tokens_used=100,
            fallback_used=False
        )
        assert output.response == "Respuesta de prueba"
        assert len(output.sources) == 2
        assert output.tokens_used == 100
        assert output.fallback_used is False


class TestNormativeChainIntegration:
    """Pruebas de integración para la cadena completa."""

    @pytest.mark.asyncio
    async def test_full_pipeline_execution(self) -> None:
        """Verifica la ejecución completa del pipeline RAG."""
        with patch("app.chains.normative_chain.bedrock_runtime"):
            settings = MagicMock(spec=Settings)
            settings.aws_region = "us-east-1"
            settings.bedrock_model_id = "anthropic.claude-3-sonnet-06202025"
            settings.max_tokens = 2048
            settings.temperature = 0.7
            settings.top_k = 5
            settings.enable_rag = True

            repo = MagicMock(spec=NormativeRepository)
            repo.retrieve_relevant_documents = AsyncMock(return_value=[
                {"content": "Normativa RGPD", "score": 0.95, "source": "RGPD"}
            ])
            repo.generate_response = AsyncMock(return_value={
                "response": "Respuesta completa",
                "usage": {"inputTokens": 100, "outputTokens": 50}
            })

            chain = NormativeChain(settings=settings, repository=repo)
            input_data = ChainInput(query="Requisitos RGPD")
            result = await chain.invoke(input_data)

            assert result.response is not None
            assert len(result.sources) > 0
            assert result.tokens_used > 0

// === ARCHIVO: tests/test_eval.py ===
import pytest
import json
from pathlib import Path
from unittest.mock import MagicMock, AsyncMock, patch
from typing import Any

from app.eval.metrics import EvaluationMetrics, MetricResult
from app.eval.evaluation_dataset import EvaluationDataset, EvaluationCase
from app.config.settings import Settings
from app.chains.normative_chain import NormativeChain, ChainInput


class TestEvaluationMetrics:
    """Pruebas para las métricas de evaluación del sistema RAG."""

    @pytest.fixture
    def metrics_calculator(self) -> EvaluationMetrics:
        return EvaluationMetrics()

    def test_calculate_exact_match(self, metrics_calculator: EvaluationMetrics) -> None:
        """Verifica el cálculo de exactitud exacta entre respuesta y referencia."""
        predicted = "La normativa establece que los datos deben ser protegidos"
        reference = "La normativa establece que los datos deben ser protegidos"

        result = metrics_calculator.calculate_exact_match(predicted, reference)

        assert result.score == 1.0
        assert result.metric_name == "exact_match"

    def test_calculate_exact_match_partial(self, metrics_calculator: EvaluationMetrics) -> None:
        """Verifica exact match con coincidencia parcial."""
        predicted = "La normativa establece protección de datos"
        reference = "La normativa establece que los datos deben ser protegidos"

        result = metrics_calculator.calculate_exact_match(predicted, reference)

        assert result.score < 1.0
        assert result.score > 0.0

    def test_calculate_f1_score(self, metrics_calculator: EvaluationMetrics) -> None:
        """Verifica el cálculo del F1 score basado en tokens."""
        predicted_tokens = ["la", "normativa", "establece", "protección", "datos"]
        reference_tokens = ["la", "normativa", "establece", "que", "los", "datos", "deben", "ser", "protegidos"]

        result = metrics_calculator.calculate_f1_score(predicted_tokens, reference_tokens)

        assert result.score > 0.0
        assert result.score <= 1.0
        assert result.metric_name == "f1_score"

    def test_calculate_retrieval_precision(self, metrics_calculator: EvaluationMetrics) -> None:
        """Verifica la precisión de recuperación de documentos relevantes."""
        retrieved = ["doc1", "doc2", "doc3", "doc4"]
        relevant = ["doc1", "doc3", "doc5"]

        result = metrics_calculator.calculate_retrieval_precision(retrieved, relevant)

        assert result.score == pytest.approx(0.5, rel=0.01)

    def test_calculate_retrieval_recall(self, metrics_calculator: EvaluationMetrics) -> None:
        """Verifica el recall de recuperación de documentos relevantes."""
        retrieved = ["doc1", "doc2", "doc3"]
        relevant = ["doc1", "doc3", "doc5", "doc6"]

        result = metrics_calculator.calculate_retrieval_recall(retrieved, relevant)

        assert result.score == pytest.approx(0.5, rel=0.01)

    def test_calculate_context_relevance(self, metrics_calculator: EvaluationMetrics) -> None:
        """Verifica la relevancia del contexto recuperado."""
        context = "El RGPD establece que los datos personales deben ser protegidos"
        query = "requisitos de protección de datos"

        result = metrics_calculator.calculate_context_relevance(context, query)

        assert result.score > 0.0
        assert result.score <= 1.0
        assert result.metric_name == "context_relevance"

    def test_calculate_answer_quality(self, metrics_calculator: EvaluationMetrics) -> None:
        """Verifica la evaluación de calidad de la respuesta."""
        answer = "Según la normativa RGPD, los datos personales deben ser protegidos"
        expected_elements = ["RGPD", "datos personales", "protegidos"]

        result = metrics_calculator.calculate_answer_quality(answer, expected_elements)

        assert result.score > 0.0
        assert result.metric_name == "answer_quality"

    def test_aggregate_metrics(self, metrics_calculator: EvaluationMetrics) -> None:
        """Verifica la agregación de múltiples métricas."""
        results = [
            MetricResult(metric_name="exact_match", score=0.8, details={}),
            MetricResult(metric_name="f1_score", score=0.75, details={}),
            MetricResult(metric_name="context_relevance", score=0.9, details={}),
        ]

        aggregated = metrics_calculator.aggregate_metrics(results)

        assert aggregated["mean_score"] == pytest.approx(0.816, rel=0.01)
        assert "exact_match" in aggregated["breakdown"]


class TestEvaluationDataset:
    """Pruebas para el conjunto de datos de evaluación."""

    @pytest.fixture
    def sample_dataset(self) -> list[dict[str, Any]]:
        return [
            {
                "id": "case_001",
                "query": "¿Cuáles son los requisitos del RGPD?",
                "expected_response": "El RGPD requiere consentimiento explícito, minimization de datos, y derecho de acceso.",
                "relevant_sources": ["RGPD_Art_5", "RGPD_Art_7"],
                "expected_elements": ["RGPD", "consentimiento", "minimización", "derecho de acceso"]
            },
            {
                "id": "case_002",
                "query": "¿Cómo implementar la protección de datos?",
                "expected_response": "Implementar medidas técnicas y organizativas apropiadas.",
                "relevant_sources": ["LOPD_Art_32"],
                "expected_elements": ["medidas técnicas", "medidas organizativas"]
            }
        ]

    def test_load_dataset_from_json(self, sample_dataset: list[dict[str, Any]], tmp_path: Path) -> None:
        """Verifica la carga del dataset desde archivo JSON."""
        dataset_file = tmp_path / "evaluation_dataset.json"
        with open(dataset_file, "w") as f:
            json.dump(sample_dataset, f)

        dataset = EvaluationDataset(dataset_path=str(dataset_file))
        assert len(dataset.cases) == 2
        assert dataset.cases[0].query == "¿Cuáles son los requisitos del RGPD?"

    def test_get_case_by_id(self, sample_dataset: list[dict[str, Any]]) -> None:
        """Verifica la recuperación de un caso por ID."""
        dataset = EvaluationDataset(cases=sample_dataset)

        case = dataset.get_case_by_id("case_001")

        assert case is not None
        assert case["id"] == "case_001"

    def test_get_case_by_id_not_found(self, sample_dataset: list[dict[str, Any]]) -> None:
        """Verifica el comportamiento cuando no se encuentra el caso."""
        dataset = EvaluationDataset(cases=sample_dataset)

        case = dataset.get_case_by_id("case_999")

        assert case is None

    def test_iterate_over_cases(self, sample_dataset: list[dict[str, Any]]) -> None:
        """Verifica la iteración sobre los casos del dataset."""
        dataset = EvaluationDataset(cases=sample_dataset)

        cases_list = list(dataset)

        assert len(cases_list) == 2


class TestEvaluationIntegration:
    """Pruebas de integración para el sistema de evaluación completo."""

    @pytest.mark.asyncio
    async def test_evaluate_full_pipeline(self) -> None:
        """Verifica la evaluación del pipeline completo con casos de prueba."""
        with patch("app.eval.metrics.bedrock_runtime"):
            test_cases = [
                {
                    "id": "eval_001",
                    "query": "Requisitos de protección de datos",
                    "expected_response": "El RGPD establece requisitos de protección",
                    "relevant_sources": ["RGPD"],
                    "expected_elements": ["RGPD", "protección"]
                }
            ]

            metrics = EvaluationMetrics()
            dataset = EvaluationDataset(cases=test_cases)

            results = []
            for case in dataset:
                predicted_response = "El RGPD establece requisitos de protección de datos personales"
                reference_response = case["expected_response"]

                exact_match = metrics.calculate_exact_match(predicted_response, reference_response)
                answer_quality = metrics.calculate_answer_quality(
                    predicted_response,
                    case["expected_elements"]
                )

                results.append({
                    "case_id": case["id"],
                    "exact_match": exact_match.score,
                    "answer_quality": answer_quality.score
                })

            assert len(results) == 1
            assert results[0]["exact_match"] > 0.0
            assert results[0]["answer_quality"] > 0.0

    def test_calculate_retrieval_metrics(self) -> None:
        """Verifica el cálculo de métricas de recuperación."""
        metrics = EvaluationMetrics()

        retrieved = ["doc1", "doc2", "doc3"]
        relevant = ["doc1", "doc4", "doc5"]

        precision = metrics.calculate_retrieval_precision(retrieved, relevant)
        recall = metrics.calculate_retrieval_recall(retrieved, relevant)

        assert precision.score == pytest.approx(0.333, rel=0.01)
        assert recall.score == pytest.approx(0.333, rel=0.01)

    def test_aggregate_evaluation_results(self) -> None:
        """Verifica la agregación de resultados de evaluación."""
        metrics = EvaluationMetrics()

        individual_results = [
            MetricResult(metric_name="exact_match", score=0.8, details={}),
            MetricResult(metric_name="exact_match", score=0.9, details={}),
            MetricResult(metric_name="exact_match", score=0.7, details={}),
        ]

        aggregated = metrics.aggregate_metrics(individual_results)

        assert "mean_score" in aggregated
        assert aggregated["mean_score"] == pytest.approx(0.8, rel=0.01)
        assert aggregated["count"] == 3


// === ARCHIVO: infra/terraform/main.tf ===
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

// === ARCHIVO: infra/terraform/iam_policy.json ===
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "BedrockModelAccess",
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel",
        "bedrock:InvokeModelWithResponseStream",
        "bedrock:GetFoundationModel",
        "bedrock:ListFoundationModels",
        "bedrock:GetInferenceProfile",
        "bedrock:ListInferenceProfiles"
      ],
      "Resource": "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
    },
    {
      "Sid": "BedrockReadOnly",
      "Effect": "Allow",
      "Action": [
        "bedrock:ListCustomModels",
        "bedrock:GetCustomModel",
        "bedrock:ListPrompts",
        "bedrock:GetPrompt"
      ],
      "Resource": "*"
    },
    {
      "Sid": "S3DocumentsAccess",
      "Effect": "Allow",
      "Action": [
        "s3:GetObject",
        "s3:GetObjectVersion",
        "s3:ListBucket",
        "s3:GetBucketLocation",
        "s3:HeadBucket",
        "s3:HeadObject",
        "s3:HeadObjectVersion"
      ],
      "Resource": [
        "arn:aws:s3:::normative-rag-documents-prod-*",
        "arn:aws:s3:::normative-rag-documents-prod-*/*"
      ]
    },
    {
      "Sid": "S3WriteForUploads",
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:PutObjectAcl",
        "s3:DeleteObject",
        "s3:DeleteObjectVersion"
      ],
      "Resource": "arn:aws:s3:::normative-rag-documents-prod-*/uploads/*"
    },
    {
      "Sid": "DynamoDBEvaluations",
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:UpdateItem",
        "dynamodb:DeleteItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:BatchGetItem",
        "dynamodb:BatchWriteItem",
        "dynamodb:DescribeTable",
        "dynamodb:ListTables"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:*:table/normative-rag-evaluations-prod",
        "arn:aws:dynamodb:us-east-1:*:table/normative-rag-evaluations-prod/index/*"
      ]
    },
    {
      "Sid": "DynamoDBQueryHistory",
      "Effect": "Allow",
      "Action": [
        "dynamodb:GetItem",
        "dynamodb:PutItem",
        "dynamodb:Query"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:*:table/normative-rag-query-history",
        "arn:aws:dynamodb:us-east-1:*:table/normative-rag-query-history/index/*"
      ]
    },
    {
      "Sid": "OpenSearchServerlessAccess",
      "Effect": "Allow",
      "Action": [
        "aoss:APIAccess",
        "aoss:ListCollections",
        "aoss:DescribeCollection",
        "aoss:ListAccessPolicies",
        "aoss:ListSecurityPolicies",
        "aoss:ListTagsForResource"
      ],
      "Resource": "*"
    },
    {
      "Sid": "OpenSearchVectorSearch",
      "Effect": "Allow",
      "Action": [
        "aoss:CreateIndex",
        "aoss:DeleteIndex",
        "aoss:UpdateIndex",
        "aoss:Search",
        "aoss:BulkSearch",
        "aoss:BulkWrite",
        "aoss:GetIndex",
        "aoss:ListIndexes",
        "aoss:CreateDocument",
        "aoss:DeleteDocument",
        "aoss:UpdateDocument",
        "aoss:GetDocument"
      ],
      "Resource": "arn:aws:aoss:us-east-1:*:collection/normative-rag-vectors"
    },
    {
      "Sid": "CloudWatchLogs",
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents",
        "logs:DescribeLogGroups",
        "logs:DescribeLogStreams",
        "logs:GetLogEvents",
        "logs:FilterLogEvents"
      ],
      "Resource": [
        "arn:aws:logs:us-east-1:*:log-group:/aws/lambda/normative-rag-api-prod*",
        "arn:aws:logs:us-east-1:*:log-group:/aws/apigateway/normative-rag-api-prod*"
      ]
    },
    {
      "Sid": "CloudWatchMetrics",
      "Effect": "Allow",
      "Action": [
        "cloudwatch:PutMetricData",
        "cloudwatch:GetMetricStatistics",
        "cloudwatch:ListMetrics",
        "cloudwatch:DescribeAlarms"
      ],
      "Resource": "*"
    },
    {
      "Sid": "XRayReadOnly",
      "Effect": "Allow",
      "Action": [
        "xray:PutTraceSegments",
        "xray:PutTelemetryRecords",
        "xray:GetSamplingRules",
        "xray:GetSamplingTargets",
        "xray:GetSamplingStatisticSummaries"
      ],
      "Resource": "*"
    },
    {
      "Sid": "SecretsManagerAccess",
      "Effect": "Allow",
      "Action": [
        "secretsmanager:GetSecretValue",
        "secretsmanager:DescribeSecret",
        "secretsmanager:ListSecrets"
      ],
      "Resource": [
        "arn:aws:secretsmanager:us-east-1:*:secret:normative-rag/*",
        "arn:aws:secretsmanager:us-east-1:*:secret:bedrock-api-key-*"
      ]
    },
    {
      "Sid": "KMSDecrypt",
      "Effect": "Allow",
      "Action": [
        "kms:Decrypt",
        "kms:Encrypt",
        "kms:DescribeKey",
        "kms:GenerateDataKey",
        "kms:ReEncrypt*"
      ],
      "Resource": "arn:aws:kms:us-east-1:*:key/*"
    },
    {
      "Sid": "EventBridgeEvents",
      "Effect": "Allow",
      "Action": [
        "events:PutEvents",
        "events:DescribeEventBus",
        "events:ListRules",
        "events:ListTargetsByRule"
      ],
      "Resource": "arn:aws:events:us-east-1:*:event-bus/default"
    },
    {
      "Sid": "LambdaInvocation",
      "Effect": "Allow",
      "Action": [
        "lambda:InvokeFunction",
        "lambda:InvokeAsync"
      ],
      "Resource": [
        "arn:aws:lambda:us-east-1:*:function:normative-rag-*"
      ]
    },
    {
      "Sid": "DenyS3DeleteBucket",
      "Effect": "Deny",
      "Action": "s3:DeleteBucket",
      "Resource": "arn:aws:s3:::normative-rag-documents-prod-*",
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalTag/role": "admin"
        }
      }
    },
    {
      "Sid": "DenyDeleteEvaluationData",
      "Effect": "Deny",
      "Action": [
        "dynamodb:DeleteTable",
        "dynamodb:DeleteItem"
      ],
      "Resource": [
        "arn:aws:dynamodb:us-east-1:*:table/normative-rag-evaluations-prod"
      ],
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalTag/role": "admin"
        }
      }
    },
    {
      "Sid": "DenyModifyIAM",
      "Effect": "Deny",
      "Action": [
        "iam:CreateRole",
        "iam:DeleteRole",
        "iam:AttachRolePolicy",
        "iam:DetachRolePolicy",
        "iam:PutRolePolicy",
        "iam:DeleteRolePolicy"
      ],
      "Resource": "arn:aws:iam::*:role/normative-rag-*",
      "Condition": {
        "StringNotEquals": {
          "aws:PrincipalTag/role": "admin"
        }
      }
    }
  ],
  "Description": "Política IAM para el sistema de respuestas normativas con modelos generativos. Otorga acceso a Bedrock, S3, DynamoDB, OpenSearch Serverless, CloudWatch y Secrets Manager.",
  "Name": "normative-rag-lambda-policy-prod",
  "Tags": {
    "Project": "normative-rag-system",
    "Environment": "prod",
    "ManagedBy": "terraform",
    "CostCenter": "Cumplimiento"
  }
}

// === ARCHIVO: Dockerfile ===
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
// === ARCHIVO: docker-compose.yml ===
version: '3.13'

services:
  # FastAPI application service
  app:
    build:
      context: .
      dockerfile: Dockerfile
      target: development
    container_name: normative-rag-app
    ports:
      - "8000:8000"
    environment:
      - PYTHON_ENV=development
      - LOG_LEVEL=DEBUG
      - AWS_REGION=us-east-1
      - AWS_ACCESS_KEY_ID=${AWS_ACCESS_KEY_ID:-}
      - AWS_SECRET_ACCESS_KEY=${AWS_SECRET_ACCESS_KEY:-}
      - S3_BUCKET_NAME=${S3_BUCKET_NAME:-normative-documents}
      - EMBEDDING_MODEL_ID=amazon.titan-embed-text-v1
      - GENERATION_MODEL_ID=anthropic.claude-3-sonnet-20240229-v1:0
      - VECTOR_DB_HOST=qdrant
      - VECTOR_DB_PORT=6333
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    volumes:
      - ./app:/app/app
      - ./tests:/app/tests
      - ./data:/app/data
      - ~/.aws:/home/appuser/.aws:ro
    depends_on:
      qdrant:
        condition: service_healthy
      redis:
        condition: service_started
    networks:
      - rag-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  # Qdrant vector database for RAG embeddings
  qdrant:
    image: qdrant/qdrant:v1.7.4
    container_name: normative-rag-qdrant
    ports:
      - "6333:6333"
      - "6334:6334"
    environment:
      - QDRANT_STORAGE__STORAGE_PATH=/qdrant/storage
      - QDRANT_SERVICE__GRPC_PORT=6334
      - QDRANT_SERVICE__HTTP_PORT=6333
      - QDRANT_LOG_LEVEL=INFO
    volumes:
      - qdrant-data:/qdrant/storage
    networks:
      - rag-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:6333/health"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 30s

  # Redis cache for session management and rate limiting
  redis:
    image: redis:7.2-alpine
    container_name: normative-rag-redis
    ports:
      - "6379:6379"
    command: redis-server --appendonly yes --maxmemory 256mb --maxmemory-policy allkeys-lru
    volumes:
      - redis-data:/data
    networks:
      - rag-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "redis-cli", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
      start_period: 10s

  # LocalStack for AWS service emulation in development
  localstack:
    image: localstack/localstack:3.0
    container_name: normative-rag-localstack
    ports:
      - "4566:4566"
    environment:
      - SERVICES=s3,lambda,sts
      - DEBUG=1
      - DATA_DIR=/tmp/localstack/data
      - DEFAULT_REGION=us-east-1
      - LAMBDA_EXECUTOR=local
      - DOCKER_HOST=unix:///var/run/docker.sock
    volumes:
      - "/var/run/docker.sock:/var/run/docker.sock"
      - localstack-data:/tmp/localstack
    networks:
      - rag-network
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4566/_localstack/health"]
      interval: 30s
      timeout: 15s
      retries: 10
      start_period: 60s

  # Prometheus for metrics collection
  prometheus:
    image: prom/prometheus:v2.50.1
    container_name: normative-rag-prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./infra/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro
      - prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
      - '--storage.tsdb.retention.time=30d'
    networks:
      - rag-network
    restart: unless-stopped

  # Grafana for visualization and monitoring dashboards
  grafana:
    image: grafana/grafana:10.3.1
    container_name: normative-rag-grafana
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_USER=admin
      - GF_SECURITY_ADMIN_PASSWORD=admin
      - GF_USERS_ALLOW_SIGN_UP=false
    volumes:
      - ./infra/grafana/dashboards:/etc/grafana/provisioning/dashboards:ro
      - ./infra/grafana/datasources:/etc/grafana/provisioning/datasources:ro
      - grafana-data:/var/lib/grafana
    networks:
      - rag-network
    restart: unless-stopped
    depends_on:
      - prometheus

networks:
  rag-network:
    driver: bridge
    ipam:
      config:
        - subnet: 172.28.0.0/16

volumes:
  qdrant-data:
    driver: local
  redis-data:
    driver: local
  localstack-data:
    driver: local
  prometheus-data:
    driver: local
  grafana-data:
    driver: local

# Development workflow:
# 1. Start services: docker-compose up -d
# 2. Check health: docker-compose ps
# 3. View logs: docker-compose logs -f app
# 4. Stop services: docker-compose down
# 5. Rebuild app: docker-compose build app

# Production workflow:
# 1. Use production target: docker build --target production -t normative-rag:prod .
# 2. Update image in docker-compose.prod.yml
# 3. Deploy: docker-compose -f docker-compose.prod.yml up -d

# Environment file for local development
# Create .env file with your AWS credentials:
# AWS_ACCESS_KEY_ID=your_key_here
# AWS_SECRET_ACCESS_KEY=your_secret_here
# S3_BUCKET_NAME=normative-documents


// === ARCHIVO: app/eval/metrics.py ===
"""Métricas de evaluación para el sistema RAG de consulta normativa."""

import logging
import re
from typing import Any

import numpy as np
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class MetricResult(BaseModel):
    """Resultado de una métrica individual."""

    metric_name: str
    score: float
    details: dict[str, Any] = {}


class EvaluationMetrics:
    """Calcula métricas de evaluación para respuestas del sistema RAG."""

    def __init__(self, dataset_path: str | None = None) -> None:
        self.dataset_path = dataset_path
        self._dataset = None
        if dataset_path:
            self._load_dataset(dataset_path)

    def _load_dataset(self, path: str) -> None:
        """Carga el dataset de evaluación desde un archivo JSON."""
        import json
        from pathlib import Path

        try:
            with open(Path(path)) as f:
                self._dataset = json.load(f)
            logger.info(f"Dataset de evaluación cargado desde {path}")
        except Exception as e:
            logger.warning(f"No se pudo cargar dataset desde {path}: {e}")
            self._dataset = []

    def calculate_keyword_precision(
        self,
        predicted: str,
        reference: str,
    ) -> MetricResult:
        """Calcula precisión basada en palabras clave."""
        pred_tokens = set(predicted.lower().split())
        ref_tokens = set(reference.lower().split())

        if not pred_tokens:
            return MetricResult(metric_name="keyword_precision", score=0.0)

        matches = pred_tokens & ref_tokens
        precision = len(matches) / len(pred_tokens)

        return MetricResult(
            metric_name="keyword_precision",
            score=precision,
            details={"matches": list(matches), "total_predicted": len(pred_tokens)},
        )

    def calculate_pattern_match(
        self,
        predicted: str,
        reference: str,
    ) -> MetricResult:
        """Calcula coincidencia de patrones entre predicción y referencia."""
        ref_patterns = re.findall(r'\b\w+\b', reference.lower())
        pred_patterns = re.findall(r'\b\w+\b', predicted.lower())

        if not ref_patterns:
            return MetricResult(metric_name="pattern_match", score=0.0)

        matches = sum(1 for p in pred_patterns if p in ref_patterns)
        score = matches / len(ref_patterns)

        return MetricResult(
            metric_name="pattern_match",
            score=score,
            details={"matched": matches, "total_reference": len(ref_patterns)},
        )

    def calculate_context_relevance(
        self,
        context: str,
        query: str,
    ) -> MetricResult:
        """Calcula relevancia del contexto recuperado respecto a la consulta."""
        context_lower = context.lower()
        query_lower = query.lower()
        query_terms = set(query_lower.split())

        if not query_terms:
            return MetricResult(metric_name="context_relevance", score=0.0)

        context_terms = set(context_lower.split())
        matches = query_terms & context_terms
        relevance = len(matches) / len(query_terms)

        return MetricResult(
            metric_name="context_relevance",
            score=relevance,
            details={"matching_terms": list(matches), "query_terms": len(query_terms)},
        )

    def calculate_retrieval_precision_at_k(
        self,
        retrieved_docs: list[str],
        relevant_docs: list[str],
        k: int | None = None,
    ) -> MetricResult:
        """Calcula precisión de recuperación en los primeros k documentos."""
        if k is not None:
            retrieved_docs = retrieved_docs[:k]

        if not retrieved_docs:
            return MetricResult(metric_name="retrieval_precision_at_k", score=0.0)

        relevant_set = set(relevant_docs)
        retrieved_set = set(retrieved_docs)
        true_positives = len(retrieved_set & relevant_set)

        precision = true_positives / len(retrieved_docs)

        return MetricResult(
            metric_name="retrieval_precision_at_k",
            score=precision,
            details={"true_positives": true_positives, "retrieved": len(retrieved_docs)},
        )

    def calculate_exact_match(
        self,
        predicted: str,
        reference: str,
    ) -> MetricResult:
        """Calcula exactitud exacta (exact match) entre respuesta y referencia."""
        pred_normalized = predicted.strip().lower()
        ref_normalized = reference.strip().lower()

        if pred_normalized == ref_normalized:
            return MetricResult(metric_name="exact_match", score=1.0)

        pred_tokens = set(pred_normalized.split())
        ref_tokens = set(ref_normalized.split())

        if not ref_tokens:
            return MetricResult(metric_name="exact_match", score=0.0)

        overlap = len(pred_tokens & ref_tokens)
        jaccard = overlap / len(pred_tokens | ref_tokens)

        return MetricResult(
            metric_name="exact_match",
            score=jaccard,
            details={"exact": pred_normalized == ref_normalized},
        )

    def calculate_f1_score(
        self,
        predicted_tokens: list[str],
        reference_tokens: list[str],
    ) -> MetricResult:
        """Calcula F1 score basado en tokens."""
        if not predicted_tokens or not reference_tokens:
            return MetricResult(metric_name="f1_score", score=0.0)

        pred_set = set(predicted_tokens)
        ref_set = set(reference_tokens)

        true_positives = len(pred_set & ref_set)
        false_positives = len(pred_set - ref_set)
        false_negatives = len(ref_set - pred_set)

        precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0.0
        recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0.0

        if precision + recall == 0:
            f1 = 0.0
        else:
            f1 = 2 * (precision * recall) / (precision + recall)

        return MetricResult(
            metric_name="f1_score",
            score=f1,
            details={"precision": precision, "recall": recall},
        )

    def calculate_retrieval_precision(
        self,
        retrieved: list[str],
        relevant: list[str],
    ) -> MetricResult:
        """Calcula precisión de recuperación de documentos relevantes."""
        if not retrieved:
            return MetricResult(metric_name="retrieval_precision", score=0.0)

        retrieved_set = set(retrieved)
        relevant_set = set(relevant)
        true_positives = len(retrieved_set & relevant_set)

        precision = true_positives / len(retrieved)

        return MetricResult(
            metric_name="retrieval_precision",
            score=precision,
            details={"true_positives": true_positives, "retrieved": len(retrieved)},
        )

    def calculate_retrieval_recall(
        self,
        retrieved: list[str],
        relevant: list[str],
    ) -> MetricResult:
        """Calcula recall de recuperación de documentos relevantes."""
        if not relevant:
            return MetricResult(metric_name="retrieval_recall", score=0.0)

        retrieved_set = set(retrieved)
        relevant_set = set(relevant)
        true_positives = len(retrieved_set & relevant_set)

        recall = true_positives / len(relevant_set)

        return MetricResult(
            metric_name="retrieval_recall",
            score=recall,
            details={"true_positives": true_positives, "relevant": len(relevant_set)},
        )

    def _is_relevant(self, doc1: str, doc2: str) -> bool:
        """Determina si dos documentos son relevantes entre sí."""
        doc1_lower = doc1.lower()
        doc2_lower = doc2.lower()

        doc1_terms = set(doc1_lower.split())
        doc2_terms = set(doc2_lower.split())

        if not doc1_terms or not doc2_terms:
            return False

        overlap = len(doc1_terms & doc2_terms)
        return overlap >= min(len(doc1_terms), len(doc2_terms)) * 0.5

    def calculate_response_consistency(
        self,
        response: str,
        context: str,
    ) -> MetricResult:
        """Calcula consistencia de la respuesta con el contexto."""
        response_lower = response.lower()
        context_lower = context.lower()

        response_terms = set(response_lower.split())
        context_terms = set(context_lower.split())

        if not response_terms:
            return MetricResult(metric_name="response_consistency", score=0.0)

        in_context = response_terms & context_terms
        consistency = len(in_context) / len(response_terms)

        return MetricResult(
            metric_name="response_consistency",
            score=consistency,
            details={"terms_in_context": len(in_context), "total_terms": len(response_terms)},
        )

    def calculate_answer_completeness(
        self,
        answer: str,
        expected_elements: list[str],
    ) -> MetricResult:
        """Calcula completitud de la respuesta respecto a elementos esperados."""
        if not expected_elements:
            return MetricResult(metric_name="answer_completeness", score=1.0)

        answer_lower = answer.lower()
        found_elements = [elem for elem in expected_elements if elem.lower() in answer_lower]

        completeness = len(found_elements) / len(expected_elements)

        return MetricResult(
            metric_name="answer_completeness",
            score=completeness,
            details={"found": found_elements, "expected": expected_elements},
        )

    def calculate_answer_quality(
        self,
        answer: str,
        expected_elements: list[str],
    ) -> MetricResult:
        """Evalúa la calidad de la respuesta basada en elementos esperados."""
        if not expected_elements:
            return MetricResult(metric_name="answer_quality", score=0.5)

        answer_lower = answer.lower()
        matches = 0

        for element in expected_elements:
            if element.lower() in answer_lower:
                matches += 1

        quality = matches / len(expected_elements)

        return MetricResult(
            metric_name="answer_quality",
            score=quality,
            details={"matches": matches, "expected": len(expected_elements)},
        )

    def evaluate_single_case(
        self,
        query: str,
        predicted_response: str,
        expected_response: str,
        context: str,
    ) -> dict[str, MetricResult]:
        """Evalúa un caso individual con múltiples métricas."""
        results = {}

        results["keyword_precision"] = self.calculate_keyword_precision(
            predicted_response, expected_response
        )
        results["pattern_match"] = self.calculate_pattern_match(
            predicted_response, expected_response
        )
        results["context_relevance"] = self.calculate_context_relevance(
            context, query
        )
        results["consistency"] = self.calculate_response_consistency(
            predicted_response, context
        )

        return results

    def evaluate_dataset(
        self,
        dataset: list[dict[str, Any]],
    ) -> dict[str, Any]:
        """Evalúa todo el dataset y retorna métricas agregadas."""
        all_results = []

        for case in dataset:
            query = case.get("query", "")
            predicted = case.get("predicted_response", "")
            expected = case.get("expected_response", "")
            context = case.get("context", "")

            case_results = self.evaluate_single_case(query, predicted, expected, context)
            all_results.append(case_results)

        return {
            "total_cases": len(all_results),
            "results": all_results,
            "aggregated": self._aggregate_results(all_results),
        }

    def _aggregate_results(
        self,
        results: list[dict[str, MetricResult]],
    ) -> dict[str, float]:
        """Agrega resultados de múltiples casos."""
        if not results:
            return {}

        metric_names = results[0].keys()
        aggregated = {}

        for metric_name in metric_names:
            scores = [r[metric_name].score for r in results if metric_name in r]
            if scores:
                aggregated[metric_name] = float(np.mean(scores))

        return aggregated

    def _aggregate_by_category(
        self,
        results: list[dict[str, Any]],
        category_field: str,
    ) -> dict[str, dict[str, float]]:
        """Agrega resultados por categoría."""
        categories: dict[str, list[dict[str, Any]]] = {}

        for result in results:
            category = result.get(category_field, "unknown")
            if category not in categories:
                categories[category] = []
            categories[category].append(result)

        aggregated = {}
        for category, cat_results in categories.items():
            aggregated[category] = self._aggregate_results(cat_results)

        return aggregated

    def _aggregate_by_difficulty(
        self,
        results: list[dict[str, Any]],
    ) -> dict[str, dict[str, float]]:
        """Agrega resultados por dificultad."""
        return self._aggregate_by_category(results, "difficulty")

    def aggregate_metrics(
        self,
        results: list[MetricResult],
    ) -> dict[str, Any]:
        """Agrega múltiples métricas en un resultado consolidado."""
        if not results:
            return {"mean_score": 0.0, "count": 0, "breakdown": {}}

        scores = [r.score for r in results]
        mean_score = float(np.mean(scores))

        breakdown = {}
        for result in results:
            if result.metric_name not in breakdown:
                breakdown[result.metric_name] = []
            breakdown[result.metric_name].append(result.score)

        for metric_name in breakdown:
            breakdown[metric_name] = float(np.mean(breakdown[metric_name]))

        return {
            "mean_score": mean_score,
            "count": len(results),
            "breakdown": breakdown,
        }


def load_default_dataset() -> EvaluationMetrics:
    """Carga el dataset de evaluación por defecto."""
    return EvaluationMetrics(dataset_path=None)

```
