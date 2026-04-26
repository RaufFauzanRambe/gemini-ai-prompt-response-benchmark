# Gemini AI Prompt-Response Benchmark: Evaluation Metrics

## Overview

This document defines the metrics and evaluation methodology used to assess the quality of Gemini AI prompt-response pairs in this benchmark dataset. All metrics are designed to capture multiple dimensions of response quality, ranging from factual accuracy to stylistic appropriateness.

---

## 1. Core Quality Metrics

### 1.1 Relevance Score (0-5)

Measures how well the response addresses the specific intent of the prompt.

| Score | Description |
|-------|-------------|
| 5 | Response perfectly addresses the prompt with comprehensive coverage |
| 4 | Response addresses the prompt well with minor omissions |
| 3 | Response partially addresses the prompt, missing key aspects |
| 2 | Response loosely relates to the prompt with significant gaps |
| 1 | Response is mostly irrelevant to the prompt |
| 0 | Response does not address the prompt at all |

**Calculation:** Average of human annotator scores (minimum 3 annotators per response).

### 1.2 Coherence Score (0-5)

Evaluates the logical flow and structural integrity of the response.

| Score | Description |
|-------|-------------|
| 5 | Exceptionally well-organized with clear logical progression |
| 4 | Well-structured with minor organizational issues |
| 3 | Adequately organized but with some disjointed sections |
| 2 | Poorly organized, difficult to follow the argument |
| 1 | Severely disorganized, lacks any coherent structure |
| 0 | Completely incoherent |

### 1.3 Factual Accuracy Score (0-5)

Assesses the correctness of factual claims made in the response.

| Score | Description |
|-------|-------------|
| 5 | All factual claims are accurate and well-supported |
| 4 | Nearly all claims are accurate with minor imprecisions |
| 3 | Most claims are accurate but some notable errors exist |
| 2 | Significant factual errors present throughout |
| 1 | Majority of factual claims are incorrect |
| 0 | Response contains fabricated or entirely incorrect information |

### 1.4 Completeness Score (0-5)

Measures the thoroughness of the response relative to the prompt's requirements.

| Score | Description |
|-------|-------------|
| 5 | Exhaustive coverage of all aspects mentioned in the prompt |
| 4 | Covers most aspects thoroughly with minor gaps |
| 3 | Covers the main aspects but misses secondary requirements |
| 2 | Addresses only surface-level aspects of the prompt |
| 1 | Barely addresses the prompt's requirements |
| 0 | Fails to address any requirements |

---

## 2. Advanced Metrics

### 2.1 BLEU Score (Bilingual Evaluation Understudy)

Used to evaluate text generation quality by comparing n-gram overlap with reference responses.

- **Range:** 0.0 to 1.0
- **Method:** Corpus-level BLEU with 4-gram maximum
- **Smoothing:** Method 1 (add-1 smoothing for short sentences)

### 2.2 ROUGE Score (Recall-Oriented Understudy for Gisting Evaluation)

Measures the overlap of n-grams between generated responses and reference annotations.

- **ROUGE-1:** Unigram overlap (measures content coverage)
- **ROUGE-2:** Bigram overlap (measures phrase-level coherence)
- **ROUGE-L:** Longest Common Subsequence (measures structural similarity)

### 2.3 BERTScore

Leverages contextual embeddings from BERT to compute semantic similarity.

- **Precision:** How many tokens in the generated response have matching contextual embeddings in the reference
- **Recall:** How many tokens in the reference have matching contextual embeddings in the response
- **F1:** Harmonic mean of precision and recall

### 2.4 Perplexity

Measures how well the language model predicts the response text.

- **Lower is better** — indicates more fluent and natural text
- **Calculated using a sliding window approach** with context size of 512 tokens

### 2.5 Diversity Metrics

Assesses the variety and richness of vocabulary and sentence structures.

- **Type-Token Ratio (TTR):** Unique tokens / Total tokens
- **Distinct-n:** Count of unique n-grams / Count of total n-grams
- **Self-BLEU:** Average BLEU of each response compared to all others in the same category

---

## 3. Difficulty-Specific Metrics

### 3.1 Easy Prompts

For easy-difficulty prompts, emphasis is placed on:
- **Simplicity** — Is the language accessible to a general audience?
- **Clarity** — Is the explanation straightforward without unnecessary jargon?
- **Conciseness** — Is the response appropriately brief for the question?

### 3.2 Medium Prompts

For medium-difficulty prompts, emphasis is placed on:
- **Depth** — Does the response provide sufficient detail and analysis?
- **Structure** — Is the response well-organized with clear sections or arguments?
- **Examples** — Does the response include relevant supporting examples?

### 3.3 Hard Prompts

For hard-difficulty prompts, emphasis is placed on:
- **Technical Accuracy** — Are complex concepts handled correctly?
- **Code Quality** — For programming tasks, is the code correct, efficient, and well-documented?
- **Nuance** — Does the response capture subtle distinctions and edge cases?

---

## 4. Aggregation and Reporting

### 4.1 Per-Category Scores

Each response receives scores for all applicable metrics. Category-level scores are computed as the mean across all responses in that category.

### 4.2 Overall Benchmark Score

The overall score is a weighted average:

```
Overall Score = 0.25 × Relevance + 0.20 × Coherence + 0.20 × Factual Accuracy
              + 0.15 × Completeness + 0.10 × ROUGE-L + 0.10 × BERTScore-F1
```

### 4.3 Confidence Intervals

All reported scores include 95% confidence intervals computed using bootstrapping with 1,000 resamples.

---

## 5. Inter-Annotator Agreement

### Cohen's Kappa (κ)

Used to measure agreement between pairs of human annotators:

| κ Range | Agreement Level |
|---------|----------------|
| 0.81–1.00 | Almost Perfect |
| 0.61–0.80 | Substantial |
| 0.41–0.60 | Moderate |
| 0.21–0.40 | Fair |
| 0.00–0.20 | Slight |
| < 0.00 | Poor |

Target: κ ≥ 0.60 (Substantial agreement) across all metric dimensions.

### Fleiss' Kappa

Used to measure inter-annotator agreement across three or more annotators for the same response.

---

## 6. Automated vs. Human Evaluation

| Aspect | Automated Metrics | Human Evaluation |
|--------|------------------|------------------|
| Speed | Fast, scalable | Slow, expensive |
| Consistency | Deterministic | Subject to human variation |
| Nuance | Limited | Captures subtle quality differences |
| Reference-Free | Partial (perplexity) | Possible |
| Cost | Low | High |

The benchmark uses a hybrid approach: automated metrics for continuous monitoring and human annotations for gold-standard evaluation.