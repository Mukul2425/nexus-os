from pathlib import Path


SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
}


def load_document(
    filename: str,
    content: bytes,
) -> str:

    extension = Path(filename).suffix.lower()

    if extension not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Unsupported document type: {extension}"
        )

    try:
        return content.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError(
            "Document must be UTF-8 encoded"
        ) from exc