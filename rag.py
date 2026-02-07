import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions
from sentence_transformers import SentenceTransformer

# -----------------------------
# CONFIG
# -----------------------------
CHROMA_PATH = "vector_db"
COLLECTION_NAME = "policies"

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

client = chromadb.Client(
    Settings(
        persist_directory=CHROMA_PATH,
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection(
    name=COLLECTION_NAME,
    embedding_function=embedding_function
)

# -----------------------------
# MAIN RAG FUNCTION
# -----------------------------
def policy_answer(query: str):
    total_docs = collection.count()
    print("[DEBUG] Total docs in collection:", total_docs)

    if total_docs == 0:
        return {
            "status": "refused",
            "reason": "No policy documents have been indexed.",
            "confidence": "Low"
        }

    results = collection.query(
        query_texts=[query],
        n_results=3
    )

    documents = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    print("[DEBUG] Retrieved docs:", len(documents))

    # 🔒 HARD FALLBACK (NO MORE FALSE REFUSALS)
    if not documents:
        fallback = collection.get(limit=2)
        documents = fallback.get("documents", [[]])[0]
        metadatas = fallback.get("metadatas", [[]])[0]

    if not documents:
        return {
            "status": "refused",
            "reason": "No relevant policy evidence found.",
            "confidence": "Low"
        }

    combined_text = " ".join(documents)[:1200]

    answer = (
        "According to the available policy documentation, "
        + combined_text
    )

    sources = list(
        set(meta.get("source", "Unknown") for meta in metadatas)
    )

    return {
        "status": "answered",
        "answer": answer,
        "sources": sources,
        "confidence": "Medium",
        "limitations": [
            "This response is a policy-grounded summary, not a legal interpretation.",
            "The answer is based solely on the uploaded official documents."
        ]
    }
