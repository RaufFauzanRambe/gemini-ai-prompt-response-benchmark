#!/usr/bin/env python3
"""
Gemini AI Prompt-Response Benchmark - Scoring Script
=====================================================
This script computes automated evaluation metrics for prompt-response pairs.

Usage:
    python scoring_script.py --input <path_to_responses.json> --output <path_to_scores.csv>
    python scoring_script.py --input responses/gemini_responses.json --output evaluation/scores.csv

Requirements:
    pip install nltk rouge-score sentence-transformers numpy
"""

import json
import csv
import argparse
import logging
import numpy as np
from typing import Dict, List, Tuple, Optional
from collections import Counter

# Optional imports with graceful fallback
try:
    from rouge_score import rouge_scorer
    HAS_ROUGE = True
except ImportError:
    HAS_ROUGE = False
    logging.warning("rouge-score not installed. ROUGE metrics will be skipped.")

try:
    from sentence_transformers import SentenceTransformer, util
    HAS_BERT = True
except ImportError:
    HAS_BERT = False
    logging.warning("sentence-transformers not installed. BERTScore will be skipped.")

try:
    import nltk
    nltk.download('punkt', quiet=True)
    from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
    HAS_NLTK = True
except ImportError:
    HAS_NLTK = False
    logging.warning("NLTK not installed. BLEU score will be skipped.")


class ResponseScorer:
    """Scoring engine for prompt-response quality evaluation."""

    def __init__(self, bert_model: str = "all-MiniLM-L6-v2"):
        """
        Initialize the scorer with optional BERT model for semantic similarity.

        Args:
            bert_model: Name of the sentence-transformer model to use.
        """
        self.rouge_scorer = rouge_scorer.RougeScorer(['rouge1', 'rouge2', 'rougeL'], use_stemmer=True) if HAS_ROUGE else None
        self.bert_model = SentenceTransformer(bert_model) if HAS_BERT else None
        self.smoothing = SmoothingFunction().method1 if HAS_NLTK else None

    def compute_bleu(self, response: str, reference: str) -> float:
        """
        Compute BLEU score between response and reference.

        Args:
            response: The generated response text.
            reference: The reference/human-annotated text.

        Returns:
            BLEU score between 0.0 and 1.0.
        """
        if not HAS_NLTK:
            return 0.0
        try:
            hypothesis = response.lower().split()
            reference_tokens = [reference.lower().split()]
            return sentence_bleu(reference_tokens, hypothesis, smoothing_function=self.smoothing)
        except Exception:
            return 0.0

    def compute_rouge(self, response: str, reference: str) -> Dict[str, float]:
        """
        Compute ROUGE scores (ROUGE-1, ROUGE-2, ROUGE-L).

        Args:
            response: The generated response text.
            reference: The reference/human-annotated text.

        Returns:
            Dictionary with ROUGE precision, recall, and F1 scores.
        """
        if not HAS_ROUGE:
            return {"rouge1": 0.0, "rouge2": 0.0, "rougeL": 0.0}
        try:
            scores = self.rouge_scorer.score(reference, response)
            return {
                "rouge1": scores["rouge1"].fmeasure,
                "rouge2": scores["rouge2"].fmeasure,
                "rougeL": scores["rougeL"].fmeasure,
            }
        except Exception:
            return {"rouge1": 0.0, "rouge2": 0.0, "rougeL": 0.0}

    def compute_bertscore(self, response: str, reference: str) -> Dict[str, float]:
        """
        Compute BERTScore (precision, recall, F1) using sentence embeddings.

        Args:
            response: The generated response text.
            reference: The reference/human-annotated text.

        Returns:
            Dictionary with BERTScore precision, recall, and F1.
        """
        if not HAS_BERT:
            return {"bert_precision": 0.0, "bert_recall": 0.0, "bert_f1": 0.0}
        try:
            emb_response = self.bert_model.encode(response, convert_to_tensor=True)
            emb_reference = self.bert_model.encode(reference, convert_to_tensor=True)
            precision = util.cos_sim(emb_response, emb_reference).item()
            # For token-level BERTScore, we use cosine similarity as proxy
            return {
                "bert_precision": precision,
                "bert_recall": precision,
                "bert_f1": precision,
            }
        except Exception:
            return {"bert_precision": 0.0, "bert_recall": 0.0, "bert_f1": 0.0}

    def compute_diversity(self, response: str) -> Dict[str, float]:
        """
        Compute diversity metrics for a response.

        Args:
            response: The response text to analyze.

        Returns:
            Dictionary with type-token ratio and distinct-n scores.
        """
        tokens = response.lower().split()
        if len(tokens) == 0:
            return {"ttr": 0.0, "distinct_1": 0.0, "distinct_2": 0.0}

        unique_tokens = set(tokens)
        ttr = len(unique_tokens) / len(tokens)

        # Distinct-1 (unigram)
        distinct_1 = len(unique_tokens) / len(tokens)

        # Distinct-2 (bigram)
        bigrams = list(zip(tokens[:-1], tokens[1:]))
        unique_bigrams = set(bigrams)
        distinct_2 = len(unique_bigrams) / len(bigrams) if bigrams else 0.0

        return {"ttr": ttr, "distinct_1": distinct_1, "distinct_2": distinct_2}

    def compute_length_ratio(self, response: str, reference: str) -> float:
        """
        Compute the length ratio between response and reference.

        Args:
            response: The generated response text.
            reference: The reference text.

        Returns:
            Length ratio (response length / reference length).
        """
        response_len = len(response.split())
        reference_len = len(reference.split())
        if reference_len == 0:
            return 0.0
        return min(response_len / reference_len, 2.0)  # Cap at 2.0

    def score_response(
        self,
        response: str,
        reference: Optional[str] = None,
    ) -> Dict[str, float]:
        """
        Compute all available metrics for a single response.

        Args:
            response: The generated response text.
            reference: Optional reference text for reference-based metrics.

        Returns:
            Dictionary with all computed metric scores.
        """
        scores = {}
        scores.update(self.compute_diversity(response))
        scores["response_length"] = len(response.split())

        if reference:
            scores["bleu"] = self.compute_bleu(response, reference)
            scores.update(self.compute_rouge(response, reference))
            scores.update(self.compute_bertscore(response, reference))
            scores["length_ratio"] = self.compute_length_ratio(response, reference)

        return scores


def load_responses(input_path: str) -> List[Dict]:
    """
    Load prompt-response pairs from a JSON file.

    Args:
        input_path: Path to the JSON file containing responses.

    Returns:
        List of dictionaries with prompt, response, and optional reference.
    """
    with open(input_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    if isinstance(data, dict) and "entries" in data:
        return data["entries"]
    elif isinstance(data, list):
        return data
    else:
        raise ValueError("Invalid JSON format. Expected a list or dict with 'entries' key.")


def compute_aggregate_scores(all_scores: List[Dict[str, float]]) -> Dict[str, Dict[str, float]]:
    """
    Compute aggregate statistics across all scored responses.

    Args:
        all_scores: List of score dictionaries.

    Returns:
        Dictionary with mean, std, min, and max for each metric.
    """
    if not all_scores:
        return {}

    metric_names = all_scores[0].keys()
    aggregates = {}

    for metric in metric_names:
        values = [s[metric] for s in all_scores if metric in s]
        if values:
            aggregates[metric] = {
                "mean": float(np.mean(values)),
                "std": float(np.std(values)),
                "min": float(np.min(values)),
                "max": float(np.max(values)),
                "median": float(np.median(values)),
            }

    return aggregates


def save_scores_csv(scores: List[Dict], output_path: str):
    """
    Save individual response scores to a CSV file.

    Args:
        scores: List of score dictionaries (each should include an 'id' field).
        output_path: Path to save the CSV file.
    """
    if not scores:
        logging.warning("No scores to save.")
        return

    fieldnames = list(scores[0].keys())
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(scores)


def main():
    parser = argparse.ArgumentParser(
        description="Score Gemini AI prompt-response pairs using automated metrics."
    )
    parser.add_argument(
        "--input", "-i",
        required=True,
        help="Path to JSON file with prompt-response pairs.",
    )
    parser.add_argument(
        "--output", "-o",
        required=True,
        help="Path to save the scoring results as CSV.",
    )
    parser.add_argument(
        "--reference-file", "-r",
        default=None,
        help="Path to JSON file with reference/human-annotated responses.",
    )
    parser.add_argument(
        "--bert-model",
        default="all-MiniLM-L6-v2",
        help="Sentence-transformer model for BERTScore computation.",
    )

    args = parser.parse_args()

    # Initialize scorer
    scorer = ResponseScorer(bert_model=args.bert_model)

    # Load responses
    entries = load_responses(args.input)
    logging.info(f"Loaded {len(entries)} prompt-response pairs from {args.input}")

    # Load references if provided
    references = {}
    if args.reference_file:
        ref_entries = load_responses(args.reference_file)
        for entry in ref_entries:
            references[entry.get("id", "")] = entry.get("response", "")
        logging.info(f"Loaded {len(references)} reference responses.")

    # Score each response
    all_scores = []
    for entry in entries:
        entry_id = entry.get("id", "unknown")
        response = entry.get("response", "")
        reference = references.get(entry_id)

        scores = scorer.score_response(response=response, reference=reference)
        scores["id"] = entry_id
        scores["category"] = entry.get("category", "unknown")
        scores["difficulty"] = entry.get("difficulty", "unknown")
        all_scores.append(scores)

    # Save individual scores
    save_scores_csv(all_scores, args.output)
    logging.info(f"Individual scores saved to {args.output}")

    # Compute and display aggregates
    numeric_scores = [
        {k: v for k, v in s.items() if isinstance(v, (int, float))}
        for s in all_scores
    ]
    aggregates = compute_aggregate_scores(numeric_scores)

    print("\n" + "=" * 60)
    print("AGGREGATE BENCHMARK SCORES")
    print("=" * 60)
    for metric, stats in aggregates.items():
        print(f"  {metric:25s}: {stats['mean']:.4f} ± {stats['std']:.4f}")
    print("=" * 60)

    # Save aggregates as JSON
    agg_path = args.output.replace(".csv", "_aggregates.json")
    with open(agg_path, "w", encoding="utf-8") as f:
        json.dump(aggregates, f, indent=2)
    logging.info(f"Aggregate scores saved to {agg_path}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    main()