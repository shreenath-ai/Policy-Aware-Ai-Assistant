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

# 📜 Policy-Aware AI Assistant

A responsible AI assistant designed to answer policy-related questions **only when supported by official documents**, prioritizing transparency, caution, and real-world applicability.

---

## 🚀 Project Overview

Modern AI systems often generate confident answers without verified sources, which is risky in regulated domains like healthcare, governance, and compliance.

This project addresses that gap by building a **Policy-Aware AI Assistant** that:
- Uses official policy documents as the single source of truth
- Retrieves evidence via semantic search (RAG)
- Answers **only when policy support exists**
- Safely refuses unsupported or ambiguous queries

---

## 🧠 Core Features

- 📚 Retrieval-Augmented Generation (RAG)
- 🔍 Evidence-based answering
- ❌ Safe refusal when no policy evidence exists
- 🧾 Source transparency
- 🔎 Confidence indication
- 🎨 Clean, professional UI
- ⚖️ Responsible AI guardrails

---

## 🛠️ Tech Stack

- **Language:** Python 3.11+
- **UI:** Streamlit
- **Embeddings:** SentenceTransformers (all-MiniLM-L6-v2)
- **Vector Database:** ChromaDB
- **Document Parsing:** PyPDF + manual text ingestion
- **Architecture:** RAG (Retrieval-Augmented Generation)

---

## 📅 Development Journey (Day-wise)

---

### 🟢 Day 1 – Ideation & Conceptualization

**Focus:**
- Identified hallucination risks in policy-sensitive AI use cases
- Defined the concept of a *Policy-Aware* assistant
- Scoped the solution around healthcare and governance policies (DHA, UAE laws)

**Outcome:**
- Clear problem statement
- Defined success criteria (answer only with evidence)

---

### 🟢 Day 2 – Environment Setup & Project Structure

**Focus:**
- Python virtual environment setup
- GitHub repository initialization
- Defined clean folder structure

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


**Outcome:**
- Clean, modular project foundation

---

### 🟢 Day 3 – Building the RAG Pipeline

**Focus:**
- Implemented document ingestion
- Chunked policy text and generated embeddings
- Stored embeddings in ChromaDB
- Built semantic retrieval logic

**Outcome:**
- Functional RAG backend
- Evidence retrievable from policy documents

---

### 🟢 Day 4 – Optimization & Evaluation

**Focus:**
- Debugged retrieval edge cases
- Ensured refusal when no policy evidence exists
- Tested multiple query types
- Validated safety-first behavior

**Evaluation Criteria:**
- Evidence presence
- Refusal correctness
- Stability under ambiguous queries

**Outcome:**
- Reliable and conservative system behavior

---

### 🟢 Day 5 – UI Polish & User Experience

**Focus:**
- Designed a clean, enterprise-grade interface
- Clear separation between answers and refusals
- Added confidence indicators and source transparency
- Included disclaimers for responsible usage
- Applied subtle CSS polish for a premium look

**Outcome:**
- Demo-ready professional UI
- Improved clarity and user trust

---

### 🟢 Day 6 – Robustness, Security & Guardrails

**Focus:**
- Input validation to prevent misuse
- Exception handling to avoid crashes
- Logging for observability
- Reinforced evidence-gating logic
- Prepared security and hallucination mitigation explanations

**Outcome:**
- Stable, predictable, and judge-ready application

---

## 🎤 Demo Philosophy

The system is intentionally conservative.

- If policy evidence exists → answer transparently
- If policy evidence does not exist → refuse safely

This prioritizes **trust over verbosity**.

---

## ⚠️ Disclaimer

This assistant provides **informational guidance only**, based on uploaded policy documents.  
It does **not** constitute legal, regulatory, or professional advice.

---

## 🏁 Current Status

✅ Core functionality complete  
✅ UI polished  
✅ Safety & guardrails implemented  
✅ Ready for live demo and evaluation  

---

## 📌 Future Enhancements

- OCR support for scanned PDFs
- Expanded policy coverage
- Role-based access controls
- Advanced confidence scoring

---

Built with a focus on **responsible AI**, **explainability**, and **real-world applicability**.
