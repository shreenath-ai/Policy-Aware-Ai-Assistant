import streamlit as st
from rag import policy_answer

st.set_page_config(page_title="Policy-Aware AI Assistant", layout="centered")

st.title("📜 Policy-Aware AI Assistant")
st.caption("Answers policy questions only when supported by official documents")

query = st.text_area(
    "Enter your policy-related question:",
    placeholder="Example: What happens if a company violates this policy?"
)

if st.button("Analyze"):
    if not query.strip():
        st.warning("Please enter a question.")
    else:
        result = policy_answer(query)

        if result["status"] == "refused":
            st.error("❌ Cannot answer safely")
            st.write(result["reason"])
            st.info("This system refuses to answer when policy evidence is insufficient.")
        else:
            st.success("✅ Policy-based answer")
            st.write(result["answer"])

            st.markdown("### 📄 Policy Sources")
            for src in result["sources"]:
                st.write(f"- {src}")

            st.markdown("### 🔍 Confidence Level")
            st.write(result["confidence"])
