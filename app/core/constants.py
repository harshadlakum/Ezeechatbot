NO_ANSWER_PHRASES = [
    "i don't have information",
    "not found in the knowledge base",
    "i couldn't find",
    "i cannot find",
    "no relevant information",
    "i don't know",
    "not available in the provided context",
    "outside the scope",
]

NO_ANSWER_FALLBACK = (
    "I'm sorry, I couldn't find relevant information in the uploaded knowledge base "
    "to answer your question. Please ask something related to the uploaded content."
)

SYSTEM_PROMPT_TEMPLATE = '''You are a helpful assistant. Your job is to answer the user's question using ONLY the context provided below.

Rules:
- Answer ONLY from the provided context.
- If the answer is not present in the context, respond with exactly: "I'm sorry, I couldn't find relevant information in the uploaded knowledge base to answer your question. Please ask something related to the uploaded content."
- Do not make up any information.
- Be concise and accurate.
- Do not reference the context or the document explicitly in your answer; just answer naturally.

CONTEXT:
{context}
'''
