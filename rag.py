import os

POLICY_FILE = "policies/dha_policy.txt"

KEYWORDS = [
    "phi",
    "protected health information",
    "confidential",
    "confidentiality",
    "health data",
    "dha"
]

def policy_answer(query: str):
    if not os.path.exists(POLICY_FILE):
        return {
            "status": "refused",
            "reason": "No policy documents available for analysis.",
            "confidence": "Low"
        }

    with open(POLICY_FILE, "r", encoding="utf-8") as f:
        policy_text = f.read().lower()

    query_lower = query.lower()

    # Check if query is policy-related
    if not any(keyword in query_lower for keyword in KEYWORDS):
        return {
            "status": "refused",
            "reason": "Query is not related to available policy documents.",
            "confidence": "Low"
        }

    # Build grounded answer
    answer = (
        "According to the DHA Health Data Protection and Confidentiality Policy, "
        + policy_text[:900]
    )

    return {
        "status": "answered",
        "answer": answer,
        "sources": ["dha_policy.txt"],
        "confidence": "Medium",
        "limitations": [
            "This response is generated from the uploaded policy document.",
            "This is not legal or regulatory advice."
        ]
    }
