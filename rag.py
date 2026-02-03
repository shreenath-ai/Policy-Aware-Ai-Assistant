import chromadb
from sentence_transformers import SentenceTransformer

DB_DIR = "vector_db"
COLLECTION = "policies"
SIM_THRESHOLD = 0.35

# Load embedding model
embedder = SentenceTransformer("all-MiniLM-L6-v2")

# Initialize ChromaDB
client = chromadb.Client(
    chromadb.Settings(
        persist_directory=DB_DIR,
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection(COLLECTION)



def retrieve_policy(query, top_k=3):
    query_embedding = embedder.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    if not results["documents"]:
        return None

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    if distances[0] > SIM_THRESHOLD:
        return None

    return list(zip(documents, metadatas, distances))


def policy_answer(query):
    evidence = retrieve_policy(query)

    if evidence is None:
        return {
            "status": "refused",
            "reason": "No relevant policy evidence found.",
            "confidence": "Low"
        }

    combined_text = "\n".join([e[0] for e in evidence])
    sources = list(
        set(f"{e[1]['source']} (page {e[1]['page']})" for e in evidence)
    )

    if len(combined_text.strip()) < 200:
        return {
            "status": "refused",
            "reason": "Policy evidence is insufficient or ambiguous.",
            "sources": sources,
            "confidence": "Low"
        }

    return {
        "status": "answered",
        "answer": combined_text[:600],
        "sources": sources,
        "confidence": "Medium",
        "assumptions": [
            "Uploaded policy documents are up to date",
            "No missing external policies"
        ],
        "limitations": [
            "This system does not provide legal advice",
            "Human review is recommended"
        ]
    }

