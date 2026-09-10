def test_create_memory(client):
    response = client.post(
        "/memories",
        json={
            "content": "User prefers Python.",
            "memory_type": "semantic",
            "importance": 5,
        },
    )

    assert response.status_code == 201

    data = response.json()

    assert data["content"] == "User prefers Python."
    assert data["memory_type"] == "semantic"
    assert data["importance"] == 5
    assert data["id"]


def test_list_memories(client):
    client.post(
        "/memories",
        json={
            "content": "User works on Nexus.",
        },
    )

    response = client.get("/memories")

    assert response.status_code == 200

    data = response.json()

    assert data["total"] >= 1
    assert len(data["memories"]) >= 1


def test_update_memory(client):
    create_response = client.post(
        "/memories",
        json={
            "content": "User prefers Python.",
        },
    )

    memory_id = create_response.json()["id"]

    response = client.patch(
        f"/memories/{memory_id}",
        json={
            "content": "User prefers TypeScript.",
            "importance": 5,
        },
    )

    assert response.status_code == 200

    data = response.json()

    assert data["content"] == "User prefers TypeScript."
    assert data["importance"] == 5


def test_delete_memory(client):
    create_response = client.post(
        "/memories",
        json={
            "content": "Delete this.",
        },
    )

    memory_id = create_response.json()["id"]

    response = client.delete(
        f"/memories/{memory_id}"
    )

    assert response.status_code == 204

    response = client.get(
        f"/memories/{memory_id}"
    )

    assert response.status_code == 404