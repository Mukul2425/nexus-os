# Nexus v0.7.0 RAG Evaluation Baseline

## Evaluation Dataset

Questions: 20

The dataset contains:

- Easy retrieval questions
- Cross-document questions
- Missing-answer questions
- Similar-but-wrong questions

## Retrieval Baseline

### Configuration

Embedding model: Gemini embedding model
Vector store: ChromaDB

Recommended chunk configuration:

- Chunk size: 512
- Overlap: 100

Recommended retrieval:

- Top-K: 3

### Retrieval Results

| Top-K | Hit@K |
|------:|------:|
| 1 | 83.33% |
| 3 | 100.00% |
| 5 | 100.00% |
| 10 | 100.00% |

### Chunk Size Results

| Chunk Size | Overlap | Hit@1 | Hit@3 | Hit@5 |
|-----------:|--------:|------:|------:|------:|
| 256 | 50 | 83.33% | 94.44% | 94.44% |
| 512 | 100 | 83.33% | 100.00% | 100.00% |
| 1000 | 200 | 83.33% | 100.00% | 100.00% |

## Generation Baseline

Current evaluation dataset:

- Questions: 5
- Answer relevance: 80.00%
- Groundedness: 60.00%

These values are a baseline for the current deterministic
generation-evaluation implementation.

They are not equivalent to human evaluation or an
LLM-as-a-judge score.

## Evaluation Metrics

Implemented:

- Hit@K
- Answer relevance
- Groundedness
- Context availability
- Retrieval failure identification
- Generation failure identification

## Evaluation Workflow

```text
Evaluation Dataset
        |
        v
    Retriever
        |
        v
   Top-K Chunks
        |
        v
 Retrieval Metrics
        |
        v
      Context
        |
        v
   Generation
        |
        v
 Generation Metrics