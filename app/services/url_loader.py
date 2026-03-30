import httpx
from bs4 import BeautifulSoup
from app.core.logging import logger


def load_url(url: str) -> str:
    try:
        headers = {"User-Agent": "Mozilla/5.0 (EzeeChatBot/1.0)"}
        response = httpx.get(url, headers=headers, timeout=15, follow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        result = "\n".join(lines)
        logger.info(f"URL loaded: {url} -> {len(result)} chars")
        return result
    except Exception as e:
        logger.error(f"URL loading failed: {e}")
        raise ValueError(f"Failed to fetch URL '{url}': {e}")
