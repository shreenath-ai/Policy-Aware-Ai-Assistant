import streamlit as st
from rag import policy_answer

st.set_page_config(page_title="Policy-Aware AI Assistant")

st.title("📜 Policy-Aware AI Assistant")
st.write("Answers policy questions only when supported by official documents.")

query = st.text_area(
    "Enter your policy-related question:",
    placeholder="Example: What happens if a company violates this policy?"
)

# Button click
if st.button("Analyze"):
    result = policy_answer(query)

    if result["status"] == "refused":
        st.error("❌ Cannot answer safely")
        st.write(result["reason"])
        st.write("**Confidence:**", result["confidence"])

    else:
        st.success("✅ Policy-based answer")
        st.write(result["answer"])

        st.markdown("### 📄 Sources")
        for s in result.get("sources", []):
            st.write("- ", s)

        st.write("**Confidence:**", result["confidence"])

        # Show assumptions
        st.markdown("### 🔍 Assumptions")
        for a in result.get("assumptions", []):
            st.write("- ", a)

        # Show limitations
        st.markdown("### ⚠️ Limitations")
        for l in result.get("limitations", []):
            st.write("- ", l)

