"""
LangGraph workflow for RAG
"""
from langgraph.graph import StateGraph, END
from graph.state import GraphState
from graph.nodes import RAGNodes, should_regenerate
from utils.logger import logger


class RAGWorkflow:
    """LangGraph-based RAG workflow"""

    def __init__(self):
        self.nodes = RAGNodes()
        self.graph = self._build_graph()
        logger.info("Initialized RAG workflow")

    def _build_graph(self) -> StateGraph:
        """
        Build the LangGraph workflow

        Graph flow:
        START -> retrieve_documents -> evaluate_context -> format_context -> generate_answer -> END
        """
        workflow = StateGraph(GraphState)

        # Add nodes
        workflow.add_node("retrieve_documents", self.nodes.retrieve_documents)
        workflow.add_node("evaluate_context", self.nodes.evaluate_context)
        workflow.add_node("format_context", self.nodes.format_context)
        workflow.add_node("generate_answer", self.nodes.generate_answer)

        # Set entry point
        workflow.set_entry_point("retrieve_documents")

        # Add edges
        workflow.add_edge("retrieve_documents", "evaluate_context")
        workflow.add_edge("evaluate_context", "format_context")  # Simplified flow
        workflow.add_edge("format_context", "generate_answer")
        workflow.add_edge("generate_answer", END)

        return workflow.compile()

    def query(self, question: str) -> dict:
        """
        Run the RAG workflow for a question

        Args:
            question: User's question

        Returns:
            Dict with answer and sources
        """
        logger.info(f"Processing query: {question[:100]}...")

        # Initialize state
        initial_state: GraphState = {
            "query": question,
            "retrieved_docs": [],
            "context": "",
            "answer": "",
            "sources": [],
            "should_regenerate": False
        }

        # Run the graph
        try:
            final_state = self.graph.invoke(initial_state)

            result = {
                "question": question,
                "answer": final_state["answer"],
                "sources": final_state["sources"]
            }

            logger.info("Query processed successfully")
            return result

        except Exception as e:
            logger.error(f"Error processing query: {e}")
            return {
                "question": question,
                "answer": f"Error processing query: {str(e)}",
                "sources": []
            }
