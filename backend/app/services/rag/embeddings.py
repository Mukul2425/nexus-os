from google import genai

from app.core.config import settings


client = genai.Client(
    api_key=settings.GEMINI_API_KEY
)


EMBEDDING_MODEL = "gemini-embedding-001"


def embed_text(text: str) -> list[float]:

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )

    return response.embeddings[0].values


def embed_documents(
    texts: list[str],
) -> list[list[float]]:

    return [
        embed_text(text)
        for text in texts
    ]