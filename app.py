import streamlit as st
from rag import policy_answer


# -----------------------------
# CUSTOM CSS (SUBTLE POLISH)
# -----------------------------
st.markdown("""
<style>
/* Main app background */
.stApp {
    background-color: #0e1117;
}

/* Headings */
h1, h2, h3 {
    letter-spacing: 0.3px;
}

/* Text area */
textarea {
    border-radius: 8px !important;
    border: 1px solid #2e3440 !important;
    font-size: 15px !important;
}

/* Buttons */
button[kind="primary"] {
    border-radius: 8px !important;
    font-weight: 600 !important;
    background: linear-gradient(90deg, #4f46e5, #6366f1) !important;
    border: none !important;
}

/* Success & error boxes */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
}

/* Answer box spacing */
.block-container {
    padding-top: 2rem;
}

/* Divider */
hr {
    margin: 1.5rem 0;
}
</style>
""", unsafe_allow_html=True)
  


# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(
    page_title="Policy-Aware AI Assistant",
    page_icon="📜",
    layout="centered"
)

# -----------------------------
# HEADER
# -----------------------------
st.markdown("## 📜 Policy-Aware AI Assistant")
st.caption(
    "A responsible AI assistant designed to provide policy-grounded answers with transparency and caution."
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

if analyze_btn and query.strip():
    with st.spinner("Analyzing policy documents..."):
        try:
            result = policy_answer(query)
        except Exception as e:
            st.error("⚠️ An unexpected error occurred.")
            st.caption(str(e))
            result = None

    st.divider()

    # ❌ REFUSAL STATE
    if result and result.get("status") == "refused":
        st.error("❌ Cannot answer safely")
        st.write(result.get("reason", "No relevant policy evidence found."))

        st.markdown("**Confidence Level**")
        st.progress(0.2)
        st.caption("Low")

    # ✅ ANSWER STATE
    elif result and result.get("status") == "answered":
        st.success("✅ Policy-supported answer")

        st.write(result.get("answer", ""))

        if result.get("sources"):
            st.markdown("**Sources**")
            for src in result["sources"]:
                st.write(f"- {src}")

        st.markdown("**Confidence Level**")
        st.progress(0.6)
        st.caption("Medium")

# -----------------------------
# FOOTER / DISCLAIMER
# -----------------------------
st.divider()
st.caption(
    "⚖️ Disclaimer: This assistant provides informational guidance based on uploaded policy documents. "
    "It does not constitute legal, regulatory, or professional advice."
)
