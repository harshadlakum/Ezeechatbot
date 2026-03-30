from typing import List, Dict, Any
from app.services.retriever import retrieve_relevant_chunks
from app.services.llm_service import call_llm, estimate_tokens, estimate_cost
from app.core.constants import NO_ANSWER_FALLBACK, NO_ANSWER_PHRASES
from app.core.logging import logger


def _is_unanswered(response_text: str) -> bool:
    lower = response_text.lower()
    return any(phrase in lower for phrase in NO_ANSWER_PHRASES)


def run_rag(
    bot_id: str,
    user_message: str,
    conversation_history: List[Dict],
) -> Dict[str, Any]:
    chunks = retrieve_relevant_chunks(user_message, bot_id)

    if not chunks:
        logger.info(f"No relevant chunks found for bot_id={bot_id}. Returning fallback.")
        input_tokens = estimate_tokens(user_message)
        return {
            "answer": NO_ANSWER_FALLBACK,
            "was_answered": False,
            "chunks_used": 0,
            "input_tokens": input_tokens,
            "output_tokens": estimate_tokens(NO_ANSWER_FALLBACK),
            "cost_usd": estimate_cost(input_tokens, estimate_tokens(NO_ANSWER_FALLBACK)),
        }

    context = "\n\n---\n\n".join(c["text"] for c in chunks)
    llm_result = call_llm(
        context=context,
        conversation_history=conversation_history,
        user_message=user_message,
    )
    answer = llm_result["answer"]
    was_answered = not _is_unanswered(answer)

    return {
        "answer": answer,
        "was_answered": was_answered,
        "chunks_used": len(chunks),
        "input_tokens": llm_result["input_tokens"],
        "output_tokens": llm_result["output_tokens"],
        "cost_usd": llm_result["cost_usd"],
    }
