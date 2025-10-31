"""
FastAPI routes for the knowledge assistant API
"""
from fastapi import APIRouter, HTTPException
from api.models import (
    QueryRequest,
    QueryResponse,
    FeedbackRequest,
    HealthResponse,
    Source
)
from graph.workflow import RAGWorkflow
from vector_store.pgvector_store import PgVectorStore
from utils.logger import logger
import psycopg2

router = APIRouter()

# Global instances
rag_workflow = None
vector_store = None


def initialize_workflow():
    """Initialize RAG workflow (called on startup)"""
    global rag_workflow, vector_store
    if rag_workflow is None:
        rag_workflow = RAGWorkflow()
        vector_store = PgVectorStore()
        logger.info("RAG workflow initialized")


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    try:
        if vector_store is None:
            initialize_workflow()

        doc_count = vector_store.get_document_count()

        return HealthResponse(
            status="healthy",
            database_connected=True,
            total_documents=doc_count
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            database_connected=False,
            total_documents=0
        )


@router.post("/api/v1/query", response_model=QueryResponse)
async def query_knowledge(request: QueryRequest):
    """
    Query the knowledge base with a question

    Args:
        request: Query request with question

    Returns:
        Answer with sources
    """
    if rag_workflow is None:
        initialize_workflow()

    try:
        # Run the RAG workflow
        result = rag_workflow.query(request.question)

        # Convert sources to Pydantic models
        sources = [Source(**src) for src in result["sources"]]

        return QueryResponse(
            question=result["question"],
            answer=result["answer"],
            sources=sources
        )

    except Exception as e:
        logger.error(f"Query failed: {e}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@router.post("/api/v1/feedback")
async def submit_feedback(request: FeedbackRequest):
    """
    Submit feedback for an answer

    Args:
        request: Feedback data

    Returns:
        Success message
    """
    try:
        if vector_store is None:
            initialize_workflow()

        # Store feedback in database
        query = """
            INSERT INTO feedback (query, answer, helpful, comment)
            VALUES (%s, %s, %s, %s)
        """

        with vector_store.connection.cursor() as cursor:
            cursor.execute(
                query,
                (request.query, request.answer, request.helpful, request.comment)
            )
            vector_store.connection.commit()

        logger.info(f"Feedback recorded: helpful={request.helpful}")

        return {"status": "success", "message": "Feedback recorded"}

    except Exception as e:
        logger.error(f"Failed to record feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to record feedback")
