import chromadb
from sentence_transformers import SentenceTransformer

DB_DIR = "./vector_db"
COLLECTION = "policies"

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize Chroma client (persistent)
client = chromadb.Client(
    settings=chromadb.Settings(
        persist_directory=DB_DIR,
        anonymized_telemetry=False
    )
)

# ALWAYS use get_or_create_collection
collection = client.get_or_create_collection(name=COLLECTION)


def retrieve_policy(query, top_k=3):
    query_emb = embedder.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_emb],
        n_results=top_k
    )

    # Safety checks
    if (
        not results
        or "documents" not in results
        or not results["documents"]
        or not results["documents"][0]
    ):
        return None

    docs = results["documents"][0]
    metas = results["metadatas"][0]
    distances = results["distances"][0]

    # Extra safety: distances list can be empty
    if not distances:
        return None

    # Refusal threshold
    if distances[0] > 0.4:
        return None

    return list(zip(docs, metas, distances))


def policy_answer(query):
    evidence = retrieve_policy(query)

    if evidence is None:
        return {
            "status": "refused",
            "reason": "No relevant policy evidence found"
        }

    answer_text = "\n".join([e[0] for e in evidence])
    sources = list(
        set(f"{e[1]['source']} (page {e[1]['page']})" for e in evidence)
    )

    return {
        "status": "answered",
        "answer": answer_text[:600],
        "sources": sources,
        "confidence": "Medium"
    }
