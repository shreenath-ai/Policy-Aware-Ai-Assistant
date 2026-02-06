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

"PS C:\Users\Shreenath\policy_aware_ai> & C:/Users/Shreenath/policy_aware_ai/venv/Scripts/Activate.ps1
(venv) PS C:\Users\Shreenath\policy_aware_ai> "



**Project Structure:**
policy_aware_ai/
├── app.py
├── rag.py
├── ingest.py
├── data/
│ └── manual_policies/
│ └── dha_policy.txt
├── vector_db/
└── README.md

# Policy-Aware AI Assistant

A responsible AI assistant designed to answer policy-related questions
only when supported by official documents.

## Problem
Generic AI systems often hallucinate answers in regulated domains
such as healthcare, data protection, and government policy.

## Solution
This assistant prioritizes **safety over fluency** by refusing to answer
when sufficient policy evidence is not available.

## Key Features
- Policy-grounded responses
- Conservative refusal-first logic
- Confidence indicators (Low / Medium)
- Safe failure handling
- Transparent limitations

## Tech Stack
- Python
- Streamlit
- ChromaDB
- Sentence Transformers

## Responsible AI Design
The system intentionally avoids speculative answers and demonstrates
controlled refusal behavior, reflecting real-world compliance systems.

## Disclaimer
This tool provides informational guidance based on uploaded policy
documents only. It does not constitute legal, regulatory, or
professional advice.
