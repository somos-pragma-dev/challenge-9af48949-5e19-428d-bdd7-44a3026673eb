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