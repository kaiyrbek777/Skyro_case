"""
API client for backend communication
"""
import requests
import os
from typing import Dict, Any, Optional


class APIClient:
    """Client for Skyro Knowledge Assistant API"""

    def __init__(self):
        self.base_url = os.getenv("BACKEND_URL", "http://backend:8000")

    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def query(self, question: str) -> Dict[str, Any]:
        """
        Query the knowledge base

        Args:
            question: User's question

        Returns:
            API response with answer and sources
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/query",
                json={"question": question},
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.Timeout:
            return {
                "question": question,
                "answer": "Request timed out. Please try again.",
                "sources": []
            }
        except Exception as e:
            return {
                "question": question,
                "answer": f"Error: {str(e)}",
                "sources": []
            }

    def submit_feedback(
        self,
        query: str,
        answer: str,
        helpful: bool,
        comment: Optional[str] = None
    ) -> bool:
        """
        Submit feedback for an answer

        Args:
            query: Original query
            answer: Generated answer
            helpful: Was the answer helpful?
            comment: Optional comment

        Returns:
            Success status
        """
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/feedback",
                json={
                    "query": query,
                    "answer": answer,
                    "helpful": helpful,
                    "comment": comment
                },
                timeout=10
            )
            response.raise_for_status()
            return True
        except Exception:
            return False
