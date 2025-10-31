"""
State definition for LangGraph workflow
"""
from typing import TypedDict, List, Dict, Any, Optional


class GraphState(TypedDict):
    """
    State that flows through the LangGraph nodes

    Attributes:
        query: User's original question
        retrieved_docs: Documents retrieved from vector store
        context: Formatted context for LLM
        answer: Generated answer
        sources: Source documents for citation
        should_regenerate: Flag to trigger query reformulation
    """
    query: str
    retrieved_docs: List[Dict[str, Any]]
    context: str
    answer: str
    sources: List[Dict[str, str]]
    should_regenerate: bool
