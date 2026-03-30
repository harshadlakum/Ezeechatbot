from app.core.logging import logger


def load_text(text: str) -> str:
    cleaned = text.strip()
    if not cleaned:
        raise ValueError("Provided text is empty.")
    logger.info(f"Text loaded: {len(cleaned)} chars")
    return cleaned
