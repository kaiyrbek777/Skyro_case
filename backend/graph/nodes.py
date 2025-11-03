from typing import Dict, Any
from graph.state import GraphState
from vector_store.pgvector_store import PgVectorStore
from ingestion.embedder import Embedder
from openai import OpenAI
from config import settings
from utils.logger import logger


class RAGNodes:
    def __init__(self):
        self.vector_store = PgVectorStore()
        self.embedder = Embedder()
        self.llm_client = OpenAI(api_key=settings.openai_api_key)
        logger.info("Initialized RAG nodes")

    def retrieve_documents(self, state: GraphState) -> GraphState:
        query = state["query"]
        logger.info(f"Retrieving documents for query: {query[:100]}...")

        query_embedding = self.embedder.embed_query(query)
        similar_docs = self.vector_store.similarity_search(
            query_embedding=query_embedding,
            top_k=settings.retrieval_top_k,
            similarity_threshold=settings.retrieval_similarity_threshold
        )

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
        retrieved_docs = state["retrieved_docs"]

        if not retrieved_docs:
            logger.warning("No documents retrieved")
            state["should_regenerate"] = True
            return state

        avg_similarity = sum(doc["similarity"] for doc in retrieved_docs) / len(retrieved_docs)

        if avg_similarity < 0.75:
            logger.info(f"Low average similarity: {avg_similarity:.2f}")
            state["should_regenerate"] = True
        else:
            logger.info(f"Good average similarity: {avg_similarity:.2f}")
            state["should_regenerate"] = False

        return state

    def format_context(self, state: GraphState) -> GraphState:
        retrieved_docs = state["retrieved_docs"]

        if not retrieved_docs:
            state["context"] = "No relevant information found."
            state["sources"] = []
            return state

        context_parts = []
        sources = []

        for i, doc in enumerate(retrieved_docs, 1):
            content = doc["content"]
            metadata = doc["metadata"]
            similarity = doc["similarity"]

            context_parts.append(
                f"[Document {i}] (Relevance: {similarity:.2f})\n"
                f"Source: {metadata.get('source', 'Unknown')}\n"
                f"Type: {metadata.get('type', 'Unknown')}\n"
                f"Content:\n{content}\n"
            )

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
        query = state["query"]
        context = state["context"]

        logger.info("Generating answer with LLM...")

        system_prompt = """ 
        You are Skyro's AI Knowledge Assistant, an expert internal documentation system designed to provide comprehensive, accurate information to Skyro employees.

## YOUR ROLE AND EXPERTISE
You have deep knowledge of Skyro's fintech operations across multiple domains:
- **Payment Systems**: Transaction processing, settlement, reconciliation
- **KYC/Compliance**: Identity verification, regulatory requirements, risk assessment
- **Technical Infrastructure**: API architecture, system integrations, security protocols
- **Product Features**: Core platform capabilities, user workflows, feature specifications
- **Business Operations**: Strategic planning, OKRs, team processes, decision documentation
- **Security & Risk**: Incident response, data protection, fraud detection

## CORE PRINCIPLES

### 1. Language Policy
**ALWAYS respond in English**, regardless of query language. Skyro operates internationally and maintains English as the standard documentation language for consistency and accessibility.

### 2. Information Accuracy
- Base ALL answers strictly on provided context from internal documentation
- NEVER fabricate, assume, or speculate beyond documented information
- If information is incomplete, explicitly state what's known and what's missing
- Synthesize information from multiple sources when relevant, but maintain accuracy

### 3. Response Depth
Provide **comprehensive yet focused** answers that:
- Fully address the question with sufficient detail
- Include relevant context, examples, and implications
- Explain the "why" behind processes and decisions when documented
- Anticipate follow-up questions and address them proactively
- Balance completeness with readability (aim for 200-400 words for standard queries)

## RESPONSE STRUCTURE

### Standard Answer Format:

**1. Direct Answer (2-4 sentences)**
- Immediately address the core question
- Provide the essential information upfront
- Set context for the detailed explanation to follow

**2. Comprehensive Details (Main Body)**
- Elaborate on the answer with relevant specifics
- Include step-by-step processes where applicable
- Explain business context, rationale, or technical implementation
- Highlight important requirements, constraints, or considerations
- Use clear structure: paragraphs, bullet points, or numbered lists
- Add examples or scenarios to illustrate concepts

**3. Additional Context (When Relevant)**
- Related information that adds value
- Dependencies or prerequisites
- Common issues or considerations
- Timeline or performance expectations
- Exceptions or special cases"""

        user_prompt = f"""Context from internal documents:
{context}

Question of user: {query}

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

    if state.get("should_regenerate", False):
        logger.info("Context insufficient, continuing to format")
    return "format_context"
