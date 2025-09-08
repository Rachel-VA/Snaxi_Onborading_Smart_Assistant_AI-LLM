# processing/embedder.py
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_chunks(chunks):
    """Take chunks (dicts with text + metadata) and add embeddings."""
    texts = [c["text"] for c in chunks]
    embeddings = model.encode(texts, convert_to_tensor=False)

    # Add embedding back into each chunk dict
    enriched_chunks = []
    for chunk, emb in zip(chunks, embeddings):
        enriched_chunk = dict(chunk)  # copy metadata + text
        enriched_chunk["embedding"] = emb.tolist(
        ) if hasattr(emb, "tolist") else emb
        enriched_chunks.append(enriched_chunk)

    return enriched_chunks
