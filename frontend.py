import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/query"

st.set_page_config(
    page_title="Enterprise Knowledge Intelligence Platform",
    page_icon="🏢",
    layout="wide",
)

# -----------------------------
# Sidebar
# -----------------------------

with st.sidebar:
    st.title("🏢 Enterprise RAG")

    st.markdown("---")

    st.subheader("Knowledge Base")

    st.metric("Documents", "6")
    st.metric("Chunks", "120")

    st.markdown("---")

    st.subheader("Architecture")

    st.success("Planner Agent")
    st.success("Hybrid Retrieval")
    st.success("Reflection Agent")
    st.success("Answer Agent")

    st.markdown("---")

    st.caption("Version 1.0")

# -----------------------------
# Header
# -----------------------------

st.title("Enterprise Knowledge Intelligence Platform")

st.caption(
    "Search enterprise documentation using Agentic Retrieval-Augmented Generation."
)

st.divider()

# -----------------------------
# API Key
# -----------------------------

api_key = st.text_input(
    "Groq API Key",
    type="password",
    placeholder="gsk_...",
)

query = st.text_area(
    "Ask a Question",
    placeholder="Example: What is the standard refund window for subscription services?",
    height=150,
)

# -----------------------------
# Submit
# -----------------------------

if st.button("🔍 Search Knowledge Base", use_container_width=True):

    if not api_key:
        st.error("Please enter your Groq API Key.")
        st.stop()

    if not query.strip():
        st.error("Please enter a question.")
        st.stop()

    with st.status("Running Agentic Workflow...", expanded=True) as status:

        st.write("🧠 Planner Agent")
        st.write("🔍 Hybrid Retrieval")
        st.write("🤔 Reflection Agent")
        st.write("✍️ Answer Generation")

        try:

            response = requests.post(
                API_URL,
                json={
                    "query": query,
                    "api_key": api_key,
                },
                timeout=120,
            )

            response.raise_for_status()

            data = response.json()

            status.update(
                label="Completed",
                state="complete",
            )

        except Exception as e:

            status.update(
                label="Failed",
                state="error",
            )

            st.error(str(e))
            st.stop()

    st.divider()

    st.subheader("💬 Answer")

    st.write(data["answer"])

    st.divider()

    st.subheader("📚 Citations")

    if len(data["citations"]) == 0:

        st.info("No citations returned.")

    else:

        for citation in data["citations"]:
            st.markdown(f"- {citation}")

    with st.expander("Execution Summary"):

        st.write("Planner ✔️")
        st.write("Hybrid Retrieval ✔️")
        st.write("Reflection ✔️")
        st.write("Answer Generated ✔️")