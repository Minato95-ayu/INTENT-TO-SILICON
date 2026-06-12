# INTENT-TO-SILICON: Benchmark Report v1.1

This document outlines the empirical benchmarking evaluation of the INTENT-TO-SILICON pipeline (v0.4), measuring its capability to reduce ambiguity, handle explicit negation, and prefer safe halting over unsupported generation (hallucination avoidance).

## 1. Methodology

The benchmark utilizes a synthetic dataset (`data/evaluation_dataset.csv`) comprising **121 structured natural language prompts** across the following categories:
- **Functional:** Direct technical requests.
- **Ambiguous:** Highly subjective or underspecified requests (e.g., "Build a good system").
- **Emotional:** Requests framed through user psychology (e.g., "Users are scared of payments").
- **Negation:** Explicit feature exclusion using Hindi/English negators (e.g., "Mujhe fast app chahiye lekin chat mat rakhna").
- **Mixed:** Complex sentences containing multiple overlapping constraints.

Each prompt was parsed completely headlessly (without interactive user loops) using the `run_benchmarks.py` execution script.

## 2. Experimental Results

The benchmark was executed on the `nlp_engine.py` using directional proximity heuristics and root lemma matching.

### 2.1 Overall Performance
**Total Inputs Evaluated:** 121

| Metric | Percentage | Description |
|--------|------------|-------------|
| **Direct Success (YAML Generated)** | 66.1% | The system successfully extracted requirements and emitted a structured YAML blueprint. |
| **Hard Fail (Out-of-Vocabulary)** | 32.2% | The system found no matching intent and **safely halted**. This represents a 0% hallucination rate on OOV inputs. |
| **Clarification Required** | 1.7% | The system detected ambiguity and required active disambiguation (declined by the headless script). |

*Note: The average number of disambiguation questions generated per prompt across the dataset was 0.56.*

### 2.2 Negation Handling (v0.4 Capability)
A major challenge in NLP is correctly interpreting exclusionary intent without accidentally discarding surrounding valid intent.

**Total Negation Cases Evaluated:** 20

| Metric | Result |
|--------|--------|
| Correctly Parsed | 17 |
| **Negation Accuracy** | **85.0%** |

The system successfully utilizes clause boundary splitting and directional proximity heuristics to assign negated features to an isolated `excluded_requirements` section in the YAML blueprint.

## 3. Reproducibility

To independently reproduce these metrics, clone the repository and execute the benchmarking suite:

```bash
# Ensure you are in the project root directory
cd INTENT-TO-SILICON

# Run the benchmark execution script
python experiments/run_benchmarks.py
```

The script will iterate over the dataset and output a console report identical to the metrics recorded above.
