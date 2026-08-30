from evaluation.ingest import ingest_evaluation_documents
from evaluation.runner import (
    evaluate_retrieval,
    load_questions,
)


def run_top_k_experiment():

    questions = load_questions()

    # Use the chunk configuration selected
    # from the chunk-size experiment.
    ingest_evaluation_documents(
        chunk_size=512,
        overlap=100,
    )

    print("\nTop-K Experiment")
    print("=" * 60)

    for k in [1, 3, 5, 10]:

        report = evaluate_retrieval(
            questions,
            k=k,
        )

        print(
            f"K={k} | "
            f"Hit@{k}: "
            f"{report['hit_at_k']:.2%}"
        )


if __name__ == "__main__":
    run_top_k_experiment()