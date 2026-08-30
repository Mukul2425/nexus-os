from evaluation.metrics.retrieval import hit_at_k


def test_hit_at_k_when_expected_chunk_is_found():
    results = [
        {
            "document": "wrong.md",
            "chunk_id": 0,
            "content": "Nexus uses Pinecone.",
            "distance": 0.1,
        },
        {
            "document": "rag.md",
            "chunk_id": 2,
            "content": "Nexus uses ChromaDB as its vector database.",
            "distance": 0.2,
        },
    ]

    assert hit_at_k(
        results,
        expected_source="rag.md",
        expected_chunk_contains="ChromaDB",
        k=2,
    )


def test_hit_at_k_when_expected_chunk_is_outside_k():
    results = [
        {
            "document": "wrong.md",
            "chunk_id": 0,
            "content": "Nexus uses Pinecone.",
            "distance": 0.1,
        },
        {
            "document": "rag.md",
            "chunk_id": 2,
            "content": "Nexus uses ChromaDB as its vector database.",
            "distance": 0.2,
        },
    ]

    assert not hit_at_k(
        results,
        expected_source="rag.md",
        expected_chunk_contains="ChromaDB",
        k=1,
    )


def test_hit_at_k_when_expected_chunk_is_missing():
    results = [
        {
            "document": "wrong.md",
            "chunk_id": 0,
            "content": "Nexus uses Pinecone.",
            "distance": 0.1,
        }
    ]

    assert not hit_at_k(
        results,
        expected_source="rag.md",
        expected_chunk_contains="ChromaDB",
        k=5,
    )


def test_hit_at_k_is_case_insensitive():
    results = [
        {
            "document": "rag.md",
            "chunk_id": 0,
            "content": "Nexus uses CHROMADB as its vector database.",
            "distance": 0.1,
        }
    ]

    assert hit_at_k(
        results,
        expected_source="rag.md",
        expected_chunk_contains="chromadb",
        k=1,
    )


def test_hit_at_k_with_no_expected_source():
    results = [
        {
            "document": "rag.md",
            "chunk_id": 0,
            "content": "Nexus uses ChromaDB.",
            "distance": 0.1,
        }
    ]

    assert not hit_at_k(
        results,
        expected_source=None,
        expected_chunk_contains=None,
        k=5,
    )