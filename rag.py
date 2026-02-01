import chromadb
from sentence_transformers import SentenceTransformer

DB_DIR = "vector_db"
COLLECTION = "policies"
SIM_THRESHOLD = 0.35

embedder = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client(
    chromadb.Settings(
        persist_directory=DB_DIR,
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection(name=COLLECTION)
print("🧠 Collections visible to rag:", client.list_collections())



def retrieve_policy(query, top_k=3):
    query_emb = embedder.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k
    )

    if not results["documents"]:
        return None

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    # Safety check: no results
    if not distances:
        return None

    # Similarity threshold check
    if distances[0] > SIM_THRESHOLD:
        return None

    return list(zip(docs, metas, distances))
