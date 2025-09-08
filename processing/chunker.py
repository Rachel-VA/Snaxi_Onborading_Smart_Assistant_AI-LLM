# processing/chunker.py
from langchain.text_splitter import RecursiveCharacterTextSplitter

def chunk_text(docs, chunk_size=1000, overlap=200):
    """Split documents into chunks, keeping metadata (source, page)."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap
    )
    
    chunks = []
    for doc in docs:
        text = doc["text"]
        source = doc["source"]
        page = doc["page"]

        # Split into smaller chunks
        split_texts = splitter.split_text(text)

        for i, chunk in enumerate(split_texts):
            chunks.append({
                "text": chunk,
                "source": source,
                "page": page,
                "chunk_id": f"{source}_p{page}_c{i}"
            })
    return chunks
