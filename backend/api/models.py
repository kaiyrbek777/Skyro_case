"""
Pydantic models for API requests and responses
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any


class QueryRequest(BaseModel):
    """Request model for asking questions"""
    question: str = Field(..., min_length=1, max_length=1000, description="User's question")


class Source(BaseModel):
    """Source document information"""
    source: str
    type: str
    relevance: str


class QueryResponse(BaseModel):
    """Response model for query answers"""
    question: str
    answer: str
    sources: List[Source]


class FeedbackRequest(BaseModel):
    """Request model for user feedback"""
    query: str
    answer: str
    helpful: bool
    comment: Optional[str] = None


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    database_connected: bool
    total_documents: int
    unique_documents: Optional[int] = 0
    document_types: Optional[Dict[str, int]] = {}
