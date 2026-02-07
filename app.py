import streamlit as st
from rag import policy_answer

# -----------------------------
# PAGE CONFIG (MUST BE FIRST)
# -----------------------------
st.set_page_config(
    page_title="Policy-Aware AI Assistant",
    page_icon="📜",
    layout="centered"
)

# -----------------------------
# CUSTOM CSS (FUTURISTIC POLISH)
# -----------------------------
st.markdown("""
<style>
.stApp {
    background: radial-gradient(circle at top, #0e1117 0%, #020617 60%);
    color: #e5e7eb;
}

/* Headings */
h1, h2, h3 {
    letter-spacing: 0.4px;
    font-weight: 600;
}

/* Text area */
textarea {
    border-radius: 10px !important;
    border: 1px solid #334155 !important;
    background-color: #020617 !important;
    font-size: 15px !important;
    color: #e5e7eb !important;
}

/* Buttons */
button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    background: linear-gradient(90deg, #4f46e5, #6366f1) !important;
    border: none !important;
    padding: 0.6rem 1.2rem !important;
}

/* Alerts */
div[data-testid="stAlert"] {
    border-radius: 12px !important;
}

/* Progress bar */
div[data-testid="stProgress"] > div {
    background-color: #6366f1;
}

/* Layout spacing */
.block-container {
    padding-top: 2.5rem;
}

/* Divider */
hr {
    margin: 2rem 0;
    border-color: #1e293b;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("## 📜 Policy-Aware AI Assistant")
st.caption(
    "A responsible AI assistant designed to provide policy-grounded answers with transparency, safety, and caution."
)

st.divider()

# -----------------------------
# INPUT SECTION
# -----------------------------
st.markdown("### 🧠 Ask a Policy Question")

query = st.text_area(
    label="Enter your question",
    placeholder="Example: How should Protected Health Information (PHI) be handled under the DHA policy?",
    height=120
)

analyze_btn = st.button("Analyze Policy Query")

# -----------------------------
# MAIN LOGIC (NO ERRORS HERE)
# -----------------------------
if analyze_btn:
    if not query.strip():
        st.warning("Please enter a policy-related question.")
    else:
        with st.spinner("Analyzing official policy documents..."):
            result = policy_answer(query)

        st.divider()

        if result.get("status") == "answered":
            st.success("Answer generated using official policy documents.")

            st.markdown("### 📄 Policy-Grounded Answer")
            st.write(result.get("answer", ""))

            if result.get("sources"):
                st.markdown("### 🔍 Sources")
                for src in result["sources"]:
                    st.write(f"- {src}")

            st.markdown("### 📊 Confidence Level")
            st.progress(0.6)
            st.caption(result.get("confidence", "Medium"))

            st.markdown("### ⚠️ Limitations")
            for note in result.get("limitations", []):
                st.write(f"- {note}")

        else:
            st.error("❌ Cannot answer safely")
            st.caption(result.get("reason", "No relevant policy evidence found."))
            st.progress(0.2)
            st.caption("Confidence: Low")

# -----------------------------
# FOOTER
# -----------------------------
st.divider()
st.caption(
    "⚖️ Disclaimer: This assistant provides informational guidance based solely on uploaded policy documents. "
    "It does not constitute legal, regulatory, or professional advice."
)
