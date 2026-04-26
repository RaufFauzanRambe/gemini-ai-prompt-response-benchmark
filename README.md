# Gemini AI Prompt-Response Benchmark

A comprehensive benchmark dataset for evaluating the quality of Gemini AI prompt-response pairs across 20 categories, 3 difficulty levels, and multiple evaluation metrics.

---

## Overview

**GEMINI-PRB v1.0.0** contains 50 curated prompt-response pairs designed to systematically evaluate AI model performance. Each prompt is categorized, difficulty-rated, and annotated by multiple human experts. The dataset includes processed train/validation/test splits, augmented paraphrased prompts, automated scoring tools, and cross-model comparison data with GPT-4o, Claude 3.5 Sonnet, and Llama 3 70B.

## Key Features

| Feature | Details |
|---------|---------|
| Total Prompts | 50 |
| Categories | 20 (Science, Programming, Creative Writing, Mathematics, etc.) |
| Difficulty Levels | Easy (12), Medium (24), Hard (14) |
| Data Splits | Train (35), Validation (10), Test (5) |
| Paraphrased Variants | 18 augmented prompts |
| Human Annotations | 30 annotations from 3 annotators (Fleiss' kappa = 0.72) |
| Cross-Model Comparison | Gemini 1.5 Pro vs GPT-4o vs Claude 3.5 vs Llama 3 |
| Automated Metrics | BLEU, ROUGE, BERTScore, Diversity, Perplexity |

## Directory Structure

```
gemini-ai-prompt-response-benchmark/
├── data/
│   ├── raw/                    # Original collected data
│   │   └── gemini_raw.json     # 50 raw prompt-response pairs with metadata
│   ├── processed/              # Clean, split datasets ready for ML
│   │   ├── train.csv           # 35 training samples
│   │   ├── validation.csv      # 10 validation samples
│   │   └── test.csv            # 5 test samples
│   └── augmented/              # Data augmentation
│       └── paraphrased_prompts.csv  # 18 paraphrased prompt variants
│
├── evaluation/                 # Evaluation tools & methodology
│   ├── metrics.md              # Detailed metric definitions and rubrics
│   └── scoring_script.py       # Automated scoring (BLEU, ROUGE, BERTScore)
│
├── prompts/                    # Prompt taxonomy & templates
│   ├── categories.json         # 20 category definitions with expectations
│   ├── difficulty_levels.json  # 3 difficulty level definitions
│   └── prompt_templates.txt    # Standardized prompt templates
│
├── responses/                  # Model outputs & annotations
│   ├── gemini_responses.json   # Gemini 1.5 Pro responses with quality scores
│   ├── human_annotations.csv   # Expert human evaluations
│   └── comparison_with_other_models.csv  # Cross-model comparison data
│
├── metadata/                   # Dataset metadata
│   ├── dataset_info.json       # Complete dataset documentation
│   ├── version_log.md          # Changelog and release notes
│   └── license.txt             # CC BY-SA 4.0 license
│
├── examples/                   # Usage examples
│   └── sample_usage.ipynb      # Jupyter notebook with data exploration
│
└── README.md                   # This file
```

## Quick Start

### 1. Load the Data

```python
import json
import pandas as pd

# Load raw data
with open('data/raw/gemini_raw.json', 'r') as f:
    raw_data = json.load(f)

# Load processed splits
train_df = pd.read_csv('data/processed/train.csv')
val_df = pd.read_csv('data/processed/validation.csv')
test_df = pd.read_csv('data/processed/test.csv')
```

### 2. Run Automated Evaluation

```bash
# Install dependencies
pip install nltk rouge-score sentence-transformers numpy

# Score responses
python evaluation/scoring_script.py \
    --input responses/gemini_responses.json \
    --output evaluation/scores.csv
```

### 3. Explore in Jupyter

Open `examples/sample_usage.ipynb` for a guided walkthrough of data loading, statistical analysis, and cross-model comparison.

## Dataset Categories

The benchmark covers 20 diverse categories:

- **Technical:** Science & Technology, Programming, Mathematics, Computer Networking, Database Design, Software Architecture, Software Engineering, DevOps
- **Humanities:** Creative Writing, Persuasive Writing, Professional Writing, Cultural Studies, Translation & Linguistics, Ethics & Philosophy
- **Social Sciences:** Economics & Business, Psychology, Political Science, Finance, Business & Entrepreneurship, Marketing

## Evaluation Methodology

### Human Evaluation

Each response is evaluated by 3 independent annotators on a 0-5 Likert scale across multiple dimensions:

- **Relevance** — How well the response addresses the prompt
- **Coherence** — Logical flow and structural quality
- **Factual Accuracy** — Correctness of factual claims
- **Completeness** — Thoroughness relative to prompt requirements
- **Creativity** — Originality and imaginative quality (where applicable)

### Automated Metrics

The scoring script (`evaluation/scoring_script.py`) computes:

| Metric | What It Measures |
|--------|-----------------|
| BLEU | N-gram overlap with reference (0-1) |
| ROUGE-1/2/L | Recall-oriented overlap (0-1) |
| BERTScore | Semantic similarity via embeddings (0-1) |
| Diversity (TTR) | Vocabulary richness |
| Distinct-n | N-gram diversity |

### Overall Score Formula

```
Overall = 0.25 x Relevance + 0.20 x Coherence + 0.20 x Factual Accuracy
        + 0.15 x Completeness + 0.10 x ROUGE-L + 0.10 x BERTScore-F1
```

## Baseline Results

### Gemini 1.5 Pro Performance

| Difficulty | Avg Quality Score | Avg Relevance | Avg Coherence |
|-----------|------------------|---------------|---------------|
| Easy | 4.38 | 4.67 | 4.50 |
| Medium | 4.33 | 4.60 | 4.47 |
| Hard | 4.24 | 4.57 | 4.30 |
| **Overall** | **4.32** | **4.61** | **4.43** |

### Cross-Model Comparison

| Model | Avg Score | Wins (out of 20) |
|-------|-----------|-------------------|
| Claude 3.5 Sonnet | 4.40 | 8 |
| GPT-4o | 4.35 | 6 |
| Gemini 1.5 Pro | 4.32 | 6 |
| Llama 3 70B | 3.43 | 0 |

## Data Format

### Raw Data (JSON)

```json
{
  "id": "RAW-001",
  "prompt": "Explain quantum entanglement...",
  "category": "Science & Technology",
  "difficulty": "easy",
  "response": "Quantum entanglement is...",
  "metadata": {
    "model": "gemini-1.5-pro",
    "temperature": 0.7,
    "latency_ms": 1234
  }
}
```

### Processed Data (CSV)

| Column | Type | Description |
|--------|------|-------------|
| id | string | Unique identifier |
| prompt | string | The input prompt |
| category | string | Topic category |
| difficulty | string | easy/medium/hard |
| response | string | Model response |
| response_length | int | Response length in characters |
| quality_score | float | Overall quality rating (0-5) |
| split | string | train/validation/test |

## Recommended Use Cases

1. **Model Evaluation** — Benchmark new AI models against established baselines
2. **Fine-tuning** — Use high-quality pairs to train or fine-tune language models
3. **Metric Research** — Study correlation between automated and human evaluation
4. **Prompt Engineering** — Analyze how prompt variations affect response quality
5. **Cross-Model Analysis** — Compare model strengths across categories

## Requirements

- Python 3.8+
- pandas, numpy
- nltk, rouge-score, sentence-transformers (for scoring script)

## Citation

```bibtex
@dataset{gemini_prb_2026,
  title={Gemini AI Prompt-Response Benchmark},
  author={Gemini Benchmark Team},
  year={2026},
  publisher={AI Research Division},
  version={1.0.0}
}
```

## License

This dataset is released under the **Creative Commons Attribution-ShareAlike 4.0 International (CC BY-SA 4.0)** license. See `metadata/license.txt` for full details.

## Known Limitations

- English-only prompts and responses
- Evaluation may favor longer, more detailed responses
- Creative writing evaluation is inherently subjective
- Cross-model comparisons represent a snapshot in time (models improve rapidly)

## Contributing

We welcome contributions including:
- Additional prompt-response pairs
- New evaluation metrics
- Bug fixes to the scoring script
- Translations and multilingual extensions

## Roadmap

- **v1.1.0** (Q3 2026): +50 pairs, multi-turn conversations, multilingual support
- **v2.0.0** (Q1 2027): 500+ pairs, expert annotations, adversarial prompts, interactive toolkit
