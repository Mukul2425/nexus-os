from evaluation.metrics.generation import (
    answer_contains_expected,
    is_grounded,
)


def test_answer_contains_expected():

    assert answer_contains_expected(
        "Nexus uses ChromaDB.",
        "ChromaDB",
    )


def test_answer_does_not_contain_expected():

    assert not answer_contains_expected(
        "Nexus uses Pinecone.",
        "ChromaDB",
    )


def test_grounded_answer():

    context = (
        "Nexus uses ChromaDB as its vector database."
    )

    answer = (
        "Nexus uses ChromaDB as its vector database."
    )

    assert is_grounded(
        answer,
        context,
    )


def test_empty_context_is_not_grounded():

    assert not is_grounded(
        "Nexus uses ChromaDB.",
        "",
    )


def test_empty_answer_is_not_grounded():

    assert not is_grounded(
        "",
        "Nexus uses ChromaDB.",
    )

def test_empty_context_is_not_grounded():

    assert is_grounded(
        "Nexus uses ChromaDB.",
        "",
    ) is False

def test_hallucinated_answer_is_not_grounded():

    context = "Nexus uses ChromaDB as its vector database."

    assert is_grounded(
        "Nexus uses Pinecone as its vector database.",
        context,
    ) is False