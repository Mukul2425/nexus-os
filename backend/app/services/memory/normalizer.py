import re
import string


def normalize_memory_content(content: str) -> str:
    """
    Normalize memory text for deterministic duplicate detection.

    Examples:
        "I prefer Python."
        "i   prefer   python!"
    
    Both normalize to:
        "i prefer python"
    """

    normalized = content.strip().lower()

    normalized = normalized.translate(
        str.maketrans("", "", string.punctuation)
    )

    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    )

    return normalized.strip()