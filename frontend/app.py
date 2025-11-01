"""
Streamlit UI for Skyro Knowledge Assistant
"""
import streamlit as st
from utils.api_client import APIClient
import time


# Page configuration
st.set_page_config(
    page_title="Skyro Knowledge Assistant",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize API client
@st.cache_resource
def get_api_client():
    return APIClient()

api_client = get_api_client()


# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.2rem;
        color: #666;
        margin-bottom: 2rem;
    }
    .source-box {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .feedback-text {
        font-size: 0.9rem;
        color: #888;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)


# Main UI
def main():
    """Main application interface"""

    # Header
    st.markdown('<div class="main-header">🧠 Skyro Knowledge Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-header">AI-powered internal knowledge access for fintech teams</div>', unsafe_allow_html=True)

    # Sidebar
    with st.sidebar:
        st.header("System Status")

        # Health check
        health = api_client.health_check()
        if health.get("status") == "healthy":
            st.success("✅ System Online")

            # Show user-friendly document stats
            unique_docs = health.get("unique_documents", 0)
            doc_types = health.get("document_types", {})

            st.metric("📚 Available Documents", unique_docs)

            # Show document types breakdown if available
            if doc_types:
                st.caption("**Document Types:**")
                for doc_type, stats in doc_types.items():
                    icon = "📝" if "confluence" in doc_type.lower() else "📄"
                    if "meeting" in doc_type.lower():
                        icon = "📅"
                    elif "spec" in doc_type.lower():
                        icon = "🔧"

                    # Get documents and chunks count
                    doc_count = stats.get("documents", 0)
                    chunk_count = stats.get("chunks", 0)

                    # Format display
                    st.caption(f"{icon} **{doc_type.replace('_', ' ').title()}:** {doc_count} docs")
                    st.caption(f"   ↳ {chunk_count} searchable chunks")
        else:
            st.error("❌ System Offline")
            st.write(health.get("message", "Unknown error"))

        st.divider()

        st.info("""
        This AI assistant helps you quickly find information from:

        - 📝 Confluence pages
        - 📅 Meeting notes
        - 📄 Product specs
        - 🔧 Technical docs
        """)

        st.divider()

        st.header("Example Questions")
        example_questions = [
            "What are our Q1 2024 OKRs?",
            "How does our fraud detection system work?",
            "What are the API rate limits?",
            "Tell me about the customer onboarding flow",
            "What payment gateways do we support?"
        ]

        for question in example_questions:
            if st.button(question, key=f"example_{question[:20]}", use_container_width=True):
                st.session_state.example_question = question

    # Initialize session state
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_response" not in st.session_state:
        st.session_state.last_response = None

    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

            # Show sources if available
            if "sources" in message and message["sources"]:
                with st.expander("📚 View Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"""
                        <div class="source-box">
                            <strong>Source {i}:</strong> {source['source']}<br>
                            <strong>Type:</strong> {source['type']}<br>
                            <strong>Relevance:</strong> {source['relevance']}
                        </div>
                        """, unsafe_allow_html=True)

    # Handle example question selection
    if "example_question" in st.session_state:
        user_input = st.session_state.example_question
        del st.session_state.example_question
    else:
        # Chat input
        user_input = st.chat_input("Ask a question about Skyro's internal knowledge...")

    # Process user input
    if user_input:
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Searching knowledge base..."):
                response = api_client.query(user_input)

            answer = response.get("answer", "No answer generated")
            sources = response.get("sources", [])

            st.markdown(answer)

            # Show sources
            if sources:
                with st.expander("📚 View Sources"):
                    for i, source in enumerate(sources, 1):
                        st.markdown(f"""
                        <div class="source-box">
                            <strong>Source {i}:</strong> {source['source']}<br>
                            <strong>Type:</strong> {source['type']}<br>
                            <strong>Relevance:</strong> {source['relevance']}
                        </div>
                        """, unsafe_allow_html=True)

        # Add assistant message
        st.session_state.messages.append({
            "role": "assistant",
            "content": answer,
            "sources": sources
        })

        # Store last response for feedback
        st.session_state.last_response = {
            "query": user_input,
            "answer": answer
        }

        # Force rerun to show feedback buttons
        st.rerun()

    # Feedback section (only show after last response)
    if st.session_state.last_response and len(st.session_state.messages) > 0:
        if st.session_state.messages[-1]["role"] == "assistant":
            st.divider()
            st.markdown("#### Was this answer helpful?")

            col1, col2, col3 = st.columns([1, 1, 4])

            with col1:
                if st.button("👍 Yes", key="helpful_yes"):
                    api_client.submit_feedback(
                        query=st.session_state.last_response["query"],
                        answer=st.session_state.last_response["answer"],
                        helpful=True
                    )
                    st.success("Thank you for your feedback!")
                    time.sleep(1)
                    st.session_state.last_response = None
                    st.rerun()

            with col2:
                if st.button("👎 No", key="helpful_no"):
                    api_client.submit_feedback(
                        query=st.session_state.last_response["query"],
                        answer=st.session_state.last_response["answer"],
                        helpful=False
                    )
                    st.success("Thank you for your feedback!")
                    time.sleep(1)
                    st.session_state.last_response = None
                    st.rerun()

    # Footer
    st.divider()
    st.markdown(
        '<div class="feedback-text">💡 Tip: Be specific in your questions for better results</div>',
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
