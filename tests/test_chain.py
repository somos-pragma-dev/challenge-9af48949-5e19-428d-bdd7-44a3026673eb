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