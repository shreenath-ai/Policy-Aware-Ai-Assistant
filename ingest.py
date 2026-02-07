import os
from pypdf import PdfReader
from sentence_transformers import SentenceTransformer
import chromadb

# -----------------------------
# CONFIG
# -----------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
VECTOR_DB_DIR = os.path.join(BASE_DIR, "vector_db")
COLLECTION_NAME = "policies"

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100

# -----------------------------
# INITIALIZE EMBEDDINGS & DB
# -----------------------------
print("🔃Loading embedding model...")
embedder = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.Client(
    chromadb.Settings(
        persist_directory=VECTOR_DB_DIR,
        anonymized_telemetry=False
    )
)

collection = client.get_or_create_collection(COLLECTION_NAME)

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def chunk_text(text, size, overlap):
    chunks = []
    start = 0
    while start < len(text):
        end = start + size
        chunks.append(text[start:end])
        start += size - overlap
    return chunks


def load_text_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def load_pdf_text(path):
    text = ""
    reader = PdfReader(path)
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"
    return text


# -----------------------------
# INGESTION PIPELINE
# -----------------------------
doc_count = 0

for root, _, files in os.walk(DATA_DIR):
    for file in files:
        file_path = os.path.join(root, file)

        # Load text based on file type
        if file.endswith(".txt"):
            print(f"Loading TEXT file: {file}")
            text = load_text_file(file_path)

        elif file.endswith(".pdf"):
            print(f"Loading PDF file: {file}")
            text = load_pdf_text(file_path)

        else:
            continue

        if not text or len(text.strip()) < 200:
            print(f"Skipping empty or unreadable file: {file}")
            continue

        # Chunk text
        chunks = chunk_text(text, CHUNK_SIZE, CHUNK_OVERLAP)

        for i, chunk in enumerate(chunks):
            embedding = embedder.encode(chunk).tolist()

            collection.add(
                documents=[chunk],
                embeddings=[embedding],
                metadatas=[{
                    "source": file,
                    "path": file_path
                }],
                ids=[f"{file}_{i}"]
            )
            doc_count += 1

print(f"Ingestion complete. Total chunks ingested: {collection.count()}")
