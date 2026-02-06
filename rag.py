import chromadb

# -----------------------------
# CONFIG
# -----------------------------
VECTOR_DB_DIR = "vector_db"
COLLECTION_NAME = "policies"

client = chromadb.Client(
    chromadb.Settings(
        persist_directory=VECTOR_DB_DIR,
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection(COLLECTION_NAME)

# -----------------------------
# MAIN ANSWER FUNCTION
# -----------------------------
def policy_answer(query):
    query = query.strip().lower()

    # Non-policy queries → refuse
    policy_keywords = [
        "policy", "law", "regulation", "data", "health",
        "confidential", "information", "protection", "phi",
        "privacy", "dha"
    ]

    if not any(word in query for word in policy_keywords):
        return {
            "status": "refused",
            "reason": "The question is not related to an official policy or regulation.",
            "confidence": "Low"
        }

    # Pull authoritative policy text directly
    docs = collection.get(limit=5)

    documents = docs.get("documents", [])
    metadatas = docs.get("metadatas", [])

    if not documents:
        return {
            "status": "refused",
            "reason": "No policy documents are available for analysis.",
            "confidence": "Low"
        }

    # Build grounded summary
    combined_text = " ".join(documents)[:1200]

    answer = (
        "According to the available policy documentation, "
        + combined_text
    )

    return {
        "status": "answered",
        "answer": answer,
        "sources": list(set(meta.get("source", "Unknown") for meta in metadatas)),
        "confidence": "Medium",
        "limitations": [
            "This response is a policy-grounded summary, not a legal interpretation.",
            "The answer is based on the uploaded official documents only."
        ]
    }

