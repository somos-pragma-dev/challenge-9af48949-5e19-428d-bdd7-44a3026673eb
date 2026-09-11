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