from unittest.mock import patch

from app.services.memory import vector_store


@patch(
    "app.services.memory.vector_store.embed_text",
    return_value=[0.1, 0.2, 0.3],
)
def test_add_memory(mock_embed):
    with patch.object(
        vector_store.collection,
        "upsert",
    ) as mock_upsert:

        vector_store.add_memory(
            memory_id="memory-1",
            content="User prefers Python.",
            memory_type="semantic",
            importance=4,
        )

        mock_embed.assert_called_once_with(
            "User prefers Python."
        )

        mock_upsert.assert_called_once()

def test_delete_memory():
    with patch.object(
        vector_store.collection,
        "delete",
    ) as mock_delete:

        vector_store.delete_memory(
            "memory-1"
        )

        mock_delete.assert_called_once()