import re
from typing import List, Dict, Any
from app.core.config import get_settings
from app.core.logging import logger

settings = get_settings()


def _split_into_sentences(text: str) -> List[str]:
    sentence_endings = re.compile(r'(?<=[.!?])\s+')
    sentences = sentence_endings.split(text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(text: str, bot_id: str, source_type: str) -> List[Dict[str, Any]]:
    chunk_size = settings.CHUNK_SIZE
    overlap = settings.CHUNK_OVERLAP

    sentences = _split_into_sentences(text)
    chunks = []
    current_chunk_words = []
    current_length = 0
    chunk_index = 0

    for sentence in sentences:
        words = sentence.split()
        sentence_len = len(sentence)

        if current_length + sentence_len > chunk_size and current_chunk_words:
            chunk_text_str = " ".join(current_chunk_words)
            chunks.append({
                "text": chunk_text_str,
                "metadata": {
                    "bot_id": bot_id,
                    "source_type": source_type,
                    "chunk_index": chunk_index,
                    "char_count": len(chunk_text_str),
                },
            })
            chunk_index += 1
            overlap_text = chunk_text_str[-overlap:] if len(chunk_text_str) > overlap else chunk_text_str
            overlap_words = overlap_text.split()
            current_chunk_words = overlap_words
            current_length = len(" ".join(current_chunk_words))

        current_chunk_words.extend(words)
        current_length += sentence_len + 1

    if current_chunk_words:
        chunk_text_str = " ".join(current_chunk_words)
        chunks.append({
            "text": chunk_text_str,
            "metadata": {
                "bot_id": bot_id,
                "source_type": source_type,
                "chunk_index": chunk_index,
                "char_count": len(chunk_text_str),
            },
        })

    logger.info(f"Chunked into {len(chunks)} chunks for bot_id={bot_id}")
    return chunks
