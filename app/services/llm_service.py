from typing import List, Dict
import ollama
from app.core.config import get_settings
from app.core.constants import SYSTEM_PROMPT_TEMPLATE
from app.core.logging import logger

settings = get_settings()


def estimate_tokens(text: str) -> int:
    return max(1, len(text) // 4)


def estimate_cost(input_tokens: int, output_tokens: int) -> float:
    input_cost = (input_tokens / 1000) * settings.COST_PER_1K_INPUT_TOKENS
    output_cost = (output_tokens / 1000) * settings.COST_PER_1K_OUTPUT_TOKENS
    return round(input_cost + output_cost, 8)


def build_prompt(context: str, conversation_history: List[Dict], user_message: str) -> List[Dict]:
    system_content = SYSTEM_PROMPT_TEMPLATE.format(context=context)
    messages = [{"role": "system", "content": system_content}]
    for turn in conversation_history[-6:]:
        messages.append({"role": turn["role"], "content": turn["content"]})
    messages.append({"role": "user", "content": user_message})
    return messages


def call_llm(
    context: str,
    conversation_history: List[Dict],
    user_message: str,
) -> Dict:
    messages = build_prompt(context, conversation_history, user_message)
    full_prompt_text = " ".join(m["content"] for m in messages)
    input_tokens = estimate_tokens(full_prompt_text)
    try:
        response = ollama.chat(
            model=settings.OLLAMA_MODEL,
            messages=messages,
            stream=False,
        )
        answer = response["message"]["content"].strip()
        output_tokens = estimate_tokens(answer)
        cost = estimate_cost(input_tokens, output_tokens)
        logger.info(
            f"LLM responded: model={settings.OLLAMA_MODEL}, "
            f"~{input_tokens} in / ~{output_tokens} out tokens"
        )
        return {
            "answer": answer,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "cost_usd": cost,
        }
    except Exception as e:
        logger.error(f"LLM call failed: {e}")
        raise RuntimeError(f"LLM call failed: {e}")
