## Policy-Aware AI Assistant

This project demonstrates a trustworthy AI system that answers
policy-related questions **only when supported by official documents**.

### Key Features
- Policy document ingestion (PDFs)
- Retrieval-Augmented Generation (RAG)
- Explicit refusal when evidence is missing
- Policy citations and confidence indicators

### How to Run
```bash
pip install -r requirements.txt
python ingest.py
streamlit run app.py

Evaluation is performed using a manually curated local test set (`tests.py`) covering valid, ambiguous, and out-of-scope queries.
