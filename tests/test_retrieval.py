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