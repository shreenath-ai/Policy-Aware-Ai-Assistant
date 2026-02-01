print("📥 INGEST SCRIPT STARTED")
import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb


DATA_DIR = "data/policies"
DB_DIR = "vector_db"
COLLECTION = "policies"

CHUNK_SIZE = 800
OVERLAP = 100

print("Loading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client(
    chromadb.Settings(
        persist_directory=DB_DIR,
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection(COLLECTION)

def chunk_text(text, size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        chunks.append(text[start:start+size])
        start += size - overlap
    return chunks

doc_count = 0

for file in os.listdir(DATA_DIR):
    if not file.endswith(".pdf"):
        continue

    print(f"Reading {file}")
    reader = PdfReader(os.path.join(DATA_DIR, file))

    for page_num, page in enumerate(reader.pages):
        text = page.extract_text()
        if not text:
            continue

        chunks = chunk_text(text, CHUNK_SIZE, OVERLAP)

        for i, chunk in enumerate(chunks):
            emb = embedder.encode(chunk).tolist()

            collection.add(
                documents=[chunk],
                embeddings=[emb],
                metadatas=[{
                    "source": file,
                    "page": page_num + 1
                }],
                ids=[f"{file}_{page_num}_{i}"]
            )
            doc_count += 1

persist_directory="./vector_db"

print(f"Ingested {doc_count} chunks.")

print("📊 Total documents stored:", doc_count)
print("📁 Vector DB path:", os.path.abspath("./vector_db"))
