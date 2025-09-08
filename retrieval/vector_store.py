# retrieval/vector_store.py
import chromadb
###from chromadb import Client
#from ollama import delete

class VectorStore:
    def __init__(self, path="data/chroma"):
        #self.persist_dir = path
        self.client = chromadb.PersistentClient(path=path)
        self.collection = self.client.get_or_create_collection("snaxi")

    def add_documents(self, chunks_with_embeddings):
        texts = [c["text"] for c in chunks_with_embeddings]
        embeddings = [c["embedding"] for c in chunks_with_embeddings]
        metadatas = [{"source": c.get("source"), "page": c.get("page")} for c in chunks_with_embeddings]
        ids = [c["chunk_id"] for c in chunks_with_embeddings]

        self.collection.add(
            documents=texts,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids
        )

    def retrieve(self, query, top_k=3):
        results = self.collection.query(query_texts=[query], n_results=top_k)
        docs = results["documents"][0]
        metas = results.get("metadatas", [[]])[0]  # ensure it's a list

        cleaned = []
        for d, m in zip(docs, metas):
            if m is None:
                m = {"source": "Unknown", "page": "N/A"}
            cleaned.append({"text": d, "metadata": m})
        return cleaned


    def clear(self):
        #delete all document from colllection in vector DB
        self.client.delete_collection("snaxi")
        self.collection = self.client.get_or_create_collection("snaxi")
       # delete all entries in the collection
        
    #def clear(self):#
        #clear chroma collection/reset Snaxi memory each time it runs
       # for coll in self.client.list_collections():
          #  self.client.delete_collection(coll.name)
