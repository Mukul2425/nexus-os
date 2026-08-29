import hashlib
import json
from pathlib import Path


CACHE_PATH = (
    Path(__file__).parent / "embedding_cache.json"
)


def _key(text: str) -> str:
    return hashlib.sha256(
        text.encode("utf-8")
    ).hexdigest()


def load_cache() -> dict:
    if not CACHE_PATH.exists():
        return {}

    with open(
        CACHE_PATH,
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def save_cache(cache: dict):
    with open(
        CACHE_PATH,
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            cache,
            file,
        )


def get_embedding(
    text: str,
    embed_function,
) -> list[float]:

    cache = load_cache()

    key = _key(text)

    if key in cache:
        return cache[key]

    embedding = embed_function(text)

    cache[key] = embedding

    save_cache(cache)

    return embedding