"""
Complete ingestion pipeline: load -> chunk -> embed -> store
"""
from typing import List
from ingestion.document_loader import DocumentLoader
from ingestion.chunker import DocumentChunker
from ingestion.embedder import Embedder
from vector_store.pgvector_store import PgVectorStore, Document
from utils.logger import logger
from config import settings


class IngestionPipeline:
    """Complete pipeline for ingesting documents into vector store"""

    def __init__(self):
        self.loader = DocumentLoader()
        self.chunker = DocumentChunker()
        self.embedder = Embedder()
        self.vector_store = PgVectorStore()

    def run(self):
        """Execute the full ingestion pipeline"""
        logger.info("=" * 60)
        logger.info("Starting document ingestion pipeline")
        logger.info("=" * 60)

        # Step 0: Clear database if configured
        if settings.clear_db_before_ingestion:
            logger.info("Step 0: Clearing existing documents from database...")
            old_count = self.vector_store.get_document_count()
            self.vector_store.clear_all_documents()
            logger.info(f"  - Cleared {old_count} existing chunks")

        # Step 1: Load documents
        logger.info("Step 1: Loading documents...")
        documents = self.loader.load_all_documents()

        if not documents:
            logger.warning("No documents found to ingest")
            return

        # Step 2: Chunk documents
        logger.info("Step 2: Chunking documents...")
        chunks = self.chunker.chunk_documents(documents)

        # Step 3: Generate embeddings
        logger.info("Step 3: Generating embeddings...")
        texts = [chunk["content"] for chunk in chunks]
        embeddings = self.embedder.embed_texts(texts)

        # Step 4: Prepare documents for storage
        logger.info("Step 4: Preparing documents for storage...")
        vector_docs = []
        for chunk, embedding in zip(chunks, embeddings):
            vector_docs.append(
                Document(
                    content=chunk["content"],
                    metadata=chunk["metadata"],
                    embedding=embedding
                )
            )

        # Step 5: Store in pgvector
        logger.info("Step 5: Storing in pgvector database...")
        doc_ids = self.vector_store.add_documents(vector_docs)

        logger.info("=" * 60)
        logger.info(f"✓ Ingestion complete!")
        logger.info(f"  - Documents loaded: {len(documents)}")
        logger.info(f"  - Chunks created: {len(chunks)}")
        logger.info(f"  - Vectors stored: {len(doc_ids)}")
        logger.info(f"  - Total documents in DB: {self.vector_store.get_document_count()}")
        logger.info("=" * 60)


def run_ingestion():
    """Standalone function to run ingestion"""
    pipeline = IngestionPipeline()
    pipeline.run()


if __name__ == "__main__":
    run_ingestion()
