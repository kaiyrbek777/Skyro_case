"""
PostgreSQL + pgvector integration for vector storage and retrieval
"""
import psycopg2
from psycopg2.extras import Json, execute_batch
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from config import settings
from utils.logger import logger


@dataclass
class Document:
    """Document with content, metadata, and optional embedding"""
    content: str
    metadata: Dict[str, Any]
    embedding: Optional[List[float]] = None
    id: Optional[int] = None


class PgVectorStore:
    """PostgreSQL + pgvector storage for document embeddings"""

    def __init__(self):
        self.connection = None
        self._connect()

    def _connect(self):
        """Establish database connection"""
        try:
            self.connection = psycopg2.connect(settings.database_url)
            logger.info("Connected to PostgreSQL database")
        except Exception as e:
            logger.error(f"Failed to connect to database: {e}")
            raise

    def add_documents(self, documents: List[Document]) -> List[int]:
        """
        Insert multiple documents with embeddings into the database

        Args:
            documents: List of Document objects with embeddings

        Returns:
            List of inserted document IDs
        """
        if not documents:
            return []

        query = """
            INSERT INTO documents (content, metadata, embedding)
            VALUES (%s, %s, %s)
            RETURNING id
        """

        inserted_ids = []
        try:
            with self.connection.cursor() as cursor:
                for doc in documents:
                    cursor.execute(
                        query,
                        (doc.content, Json(doc.metadata), doc.embedding)
                    )
                    inserted_ids.append(cursor.fetchone()[0])

                self.connection.commit()
                logger.info(f"Inserted {len(inserted_ids)} documents into database")

        except Exception as e:
            self.connection.rollback()
            logger.error(f"Failed to insert documents: {e}")
            raise

        return inserted_ids

    def similarity_search(
        self,
        query_embedding: List[float],
        top_k: int = 5,
        similarity_threshold: float = 0.7,
        metadata_filter: Optional[Dict[str, Any]] = None
    ) -> List[Document]:
        """
        Search for similar documents using cosine similarity

        Args:
            query_embedding: Query vector embedding
            top_k: Number of results to return
            similarity_threshold: Minimum similarity score (0-1)
            metadata_filter: Optional metadata filters

        Returns:
            List of similar Documents with similarity scores in metadata
        """
        # Base query
        query = """
            SELECT
                id,
                content,
                metadata,
                1 - (embedding <=> %s::vector) as similarity
            FROM documents
            WHERE 1 - (embedding <=> %s::vector) > %s
        """

        params = [query_embedding, query_embedding, similarity_threshold]

        # Add metadata filters if provided
        if metadata_filter:
            for key, value in metadata_filter.items():
                query += f" AND metadata->>'{key}' = %s"
                params.append(str(value))

        query += " ORDER BY embedding <=> %s::vector LIMIT %s"
        params.extend([query_embedding, top_k])

        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                results = cursor.fetchall()

                documents = []
                for row in results:
                    doc_id, content, metadata, similarity = row
                    metadata['similarity'] = float(similarity)
                    metadata['document_id'] = doc_id

                    documents.append(
                        Document(
                            id=doc_id,
                            content=content,
                            metadata=metadata
                        )
                    )

                logger.info(f"Found {len(documents)} similar documents")
                return documents

        except Exception as e:
            logger.error(f"Similarity search failed: {e}")
            raise

    def get_document_count(self) -> int:
        """Get total number of documents in the database"""
        query = "SELECT COUNT(*) FROM documents"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                count = cursor.fetchone()[0]
                return count
        except Exception as e:
            logger.error(f"Failed to get document count: {e}")
            return 0

    def get_stats(self) -> Dict[str, Any]:
        """Get database statistics including unique source documents"""
        try:
            with self.connection.cursor() as cursor:
                # Total chunks
                cursor.execute("SELECT COUNT(*) FROM documents")
                total_chunks = cursor.fetchone()[0]

                # Unique source documents
                cursor.execute("""
                    SELECT COUNT(DISTINCT metadata->>'source')
                    FROM documents
                    WHERE metadata->>'source' IS NOT NULL
                """)
                unique_sources = cursor.fetchone()[0]

                # Document types breakdown with both doc count and chunk count
                cursor.execute("""
                    SELECT
                        metadata->>'type' as doc_type,
                        COUNT(DISTINCT metadata->>'source') as doc_count,
                        COUNT(*) as chunk_count
                    FROM documents
                    WHERE metadata->>'type' IS NOT NULL
                    GROUP BY metadata->>'type'
                    ORDER BY chunk_count DESC
                """)
                doc_types_raw = cursor.fetchall()

                # Format as dict with both counts
                doc_types = {}
                for doc_type, doc_count, chunk_count in doc_types_raw:
                    doc_types[doc_type] = {
                        "documents": doc_count,
                        "chunks": chunk_count
                    }

                return {
                    "total_chunks": total_chunks,
                    "unique_documents": unique_sources,
                    "document_types": doc_types
                }
        except Exception as e:
            logger.error(f"Failed to get stats: {e}")
            return {
                "total_chunks": 0,
                "unique_documents": 0,
                "document_types": {}
            }

    def clear_all_documents(self):
        """Delete all documents from the database (use with caution!)"""
        query = "DELETE FROM documents"
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query)
                self.connection.commit()
                logger.warning("All documents deleted from database")
        except Exception as e:
            self.connection.rollback()
            logger.error(f"Failed to clear documents: {e}")
            raise

    def close(self):
        """Close database connection"""
        if self.connection:
            self.connection.close()
            logger.info("Database connection closed")
