import os
import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

DATA_DIR = "policies"
DB_DIR = "vector_db"
COLLECTION_NAME = "policies"

print("Loading embedding model...")
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

client = chromadb.Client(
    Settings(
        persist_directory=DB_DIR,
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection(
    name="policies"
)


documents = []
metadatas = []
ids = []

for i, filename in enumerate(os.listdir(DATA_DIR)):
    if filename.endswith(".txt"):
        path = os.path.join(DATA_DIR, filename)
        with open(path, "r", encoding="utf-8") as f:
            text = f.read().strip()

        documents.append(text)
        metadatas.append({"source": filename})
        ids.append(f"doc_{i}")

if not documents:
    raise RuntimeError("No policy documents found")

collection.add(
    documents=documents,
    metadatas=metadatas,
    ids=ids
)



print("Ingestion successful")
print("Documents added:", len(documents))

