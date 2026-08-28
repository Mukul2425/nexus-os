from evaluation.ingest import (
    ingest_evaluation_documents,
)
from evaluation.runner import (
    load_questions,
    evaluate_retrieval,
)


CHUNK_CONFIGS = [
    {
        "chunk_size": 256,
        "overlap": 50,
    },
    {
        "chunk_size": 512,
        "overlap": 100,
    },
    {
        "chunk_size": 1000,
        "overlap": 200,
    },
]


def run_chunk_size_experiment():
    questions = load_questions()

    print("\nChunk Size Experiment")
    print("=" * 60)

    for config in CHUNK_CONFIGS:
        chunk_size = config["chunk_size"]
        overlap = config["overlap"]

        print(
            f"\nChunk size: {chunk_size} "
            f"| Overlap: {overlap}"
        )

        ingest_evaluation_documents(
            chunk_size=chunk_size,
            overlap=overlap,
        )

        hit_at_1 = evaluate_retrieval(
            questions,
            k=1,
        )

        hit_at_3 = evaluate_retrieval(
            questions,
            k=3,
        )

        hit_at_5 = evaluate_retrieval(
            questions,
            k=5,
        )

        print(
            f"Hit@1: "
            f"{hit_at_1['hit_at_k']:.2%}"
        )

        print(
            f"Hit@3: "
            f"{hit_at_3['hit_at_k']:.2%}"
        )

        print(
            f"Hit@5: "
            f"{hit_at_5['hit_at_k']:.2%}"
        )


if __name__ == "__main__":
    run_chunk_size_experiment()