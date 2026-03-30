import fitz
from app.core.logging import logger


def load_pdf(file_bytes: bytes) -> str:
    try:
        doc = fitz.open(stream=file_bytes, filetype="pdf")
        pages = []
        for page in doc:
            text = page.get_text("text")
            if text.strip():
                pages.append(text.strip())
        doc.close()
        full_text = "\n\n".join(pages)
        logger.info(f"PDF loaded: {len(pages)} pages, {len(full_text)} chars")
        return full_text
    except Exception as e:
        logger.error(f"PDF loading failed: {e}")
        raise ValueError(f"Failed to parse PDF: {e}")
