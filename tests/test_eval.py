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