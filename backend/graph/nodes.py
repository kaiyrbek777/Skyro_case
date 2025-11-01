"""
LangGraph nodes for RAG workflow
"""
from typing import Dict, Any
from graph.state import GraphState
from vector_store.pgvector_store import PgVectorStore
from ingestion.embedder import Embedder
from openai import OpenAI
from config import settings
from utils.logger import logger


class RAGNodes:
    """Collection of nodes for RAG graph"""

    def __init__(self):
        self.vector_store = PgVectorStore()
        self.embedder = Embedder()
        self.llm_client = OpenAI(api_key=settings.openai_api_key)
        logger.info("Initialized RAG nodes")

    def retrieve_documents(self, state: GraphState) -> GraphState:
        """
        Node: Retrieve relevant documents from vector store

        Args:
            state: Current graph state

        Returns:
            Updated state with retrieved documents
        """
        query = state["query"]
        logger.info(f"Retrieving documents for query: {query[:100]}...")

        # Generate query embedding
        query_embedding = self.embedder.embed_query(query)

        # Search for similar documents
        similar_docs = self.vector_store.similarity_search(
            query_embedding=query_embedding,
            top_k=settings.retrieval_top_k,
            similarity_threshold=settings.retrieval_similarity_threshold
        )

        # Convert to dict format
        retrieved_docs = [
            {
                "content": doc.content,
                "metadata": doc.metadata,
                "similarity": doc.metadata.get("similarity", 0.0)
            }
            for doc in similar_docs
        ]

        logger.info(f"Retrieved {len(retrieved_docs)} documents")

        state["retrieved_docs"] = retrieved_docs
        return state

    def evaluate_context(self, state: GraphState) -> GraphState:
        """
        Node: Evaluate if retrieved context is sufficient

        Args:
            state: Current graph state

        Returns:
            Updated state with should_regenerate flag
        """
        retrieved_docs = state["retrieved_docs"]

        # Simple heuristic: check if we have enough high-quality documents
        if not retrieved_docs:
            logger.warning("No documents retrieved")
            state["should_regenerate"] = True
            return state

        # Check average similarity
        avg_similarity = sum(doc["similarity"] for doc in retrieved_docs) / len(retrieved_docs)

        if avg_similarity < 0.75:
            logger.info(f"Low average similarity: {avg_similarity:.2f}")
            state["should_regenerate"] = True
        else:
            logger.info(f"Good average similarity: {avg_similarity:.2f}")
            state["should_regenerate"] = False

        return state

    def format_context(self, state: GraphState) -> GraphState:
        """
        Node: Format retrieved documents into context string

        Args:
            state: Current graph state

        Returns:
            Updated state with formatted context
        """
        retrieved_docs = state["retrieved_docs"]

        if not retrieved_docs:
            state["context"] = "No relevant information found."
            state["sources"] = []
            return state

        # Format context
        context_parts = []
        sources = []

        for i, doc in enumerate(retrieved_docs, 1):
            content = doc["content"]
            metadata = doc["metadata"]
            similarity = doc["similarity"]

            # Add to context
            context_parts.append(
                f"[Document {i}] (Relevance: {similarity:.2f})\n"
                f"Source: {metadata.get('source', 'Unknown')}\n"
                f"Type: {metadata.get('type', 'Unknown')}\n"
                f"Content:\n{content}\n"
            )

            # Add to sources
            sources.append({
                "source": metadata.get("source", "Unknown"),
                "type": metadata.get("type", "Unknown"),
                "relevance": f"{similarity:.2f}"
            })

        state["context"] = "\n---\n".join(context_parts)
        state["sources"] = sources

        logger.info(f"Formatted context with {len(retrieved_docs)} documents")
        return state

    def generate_answer(self, state: GraphState) -> GraphState:
        """
        Node: Generate answer using LLM

        Args:
            state: Current graph state

        Returns:
            Updated state with generated answer
        """
        query = state["query"]
        context = state["context"]

        logger.info("Generating answer with LLM...")

        # Create prompt
        system_prompt = """You are a helpful AI assistant for Skyro, a fintech company.
Your role is to answer employee questions based on internal company documents.

Guidelines:
- Use ONLY the provided context to answer questions
- Be concise and accurate
- If the context doesn't contain enough information, say so
- Cite specific documents when possible
- Use a professional but friendly tone"""

        user_prompt = f"""Context from internal documents:
{context}

Question: {query}

Please provide a clear and helpful answer based on the context above."""

        try:
            response = self.llm_client.chat.completions.create(
                model=settings.llm_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens
            )

            answer = response.choices[0].message.content
            state["answer"] = answer

            logger.info("Answer generated successfully")

        except Exception as e:
            logger.error(f"Failed to generate answer: {e}")
            state["answer"] = f"Error generating answer: {str(e)}"

        return state


def should_regenerate(state: GraphState) -> str:
    """
    Conditional edge: Determine if query should be regenerated

    Args:
        state: Current graph state

    Returns:
        Next node name
    """
    if state.get("should_regenerate", False):
        logger.info("Context insufficient, would regenerate query (simplified for now)")
        # In a full implementation, this would go to a query expansion node
        # For simplicity, we'll just continue to generation
        return "format_context"
    else:
        return "format_context"
