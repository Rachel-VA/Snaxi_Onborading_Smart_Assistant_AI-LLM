import ollama

MODEL_NAME = "dolphin-mistral"


def ask_model(query, retrieved_chunks, history=None):
    """Ask the Ollama model with doc context + short history."""

    # --- Build context from retrieved chunks ---
    context_parts = []
    for chunk in retrieved_chunks:
        text = chunk.get("text", "")
        meta = chunk.get("metadata", {}) or {}
        source = meta.get("source", "Unknown source")
        page = meta.get("page", "N/A")
        context_parts.append(f"(Source: {source}, page {page})\n{text}")
    context = "\n\n".join(context_parts)

    # --- Add trimmed conversation history (last 2 turns) ---
    history_text = ""
    if history:
        for turn in history[-2:]:
            history_text += f"{turn['role'].capitalize()}: {turn['content']}\n"

    # --- Build the final prompt ---
    prompt = f"""You are Snaxi, a helpful and goofy onboarding buddy.
Your job is to answer based only on the provided context and conversation history.

Rules:
- Always cite the source and page when possible.
- Keep answers under 120 words, in short sentences or up to 3 bullet points.
- If asked to **simplify or rephrase**, do NOT change important legal keywords such as "would" vs "could".
- When simplifying, keep critical distinctions intact while making the sentences shorter and clearer.
- If rephrasing previous answers, preserve the same meaning and keywords exactly.

Conversation so far:
{history_text}

Context:
{context}

Question: {query}
Answer:"""

    # --- Call Ollama via Python client (faster) ---
    response = ollama.chat(
        model=MODEL_NAME,
        messages=[{"role": "user", "content": prompt}]
    )

    return response["message"]["content"].strip()
