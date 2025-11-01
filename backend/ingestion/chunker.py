"""
Document chunking with LangChain's text splitters
"""
from typing import List, Dict, Any
from langchain.text_splitter import RecursiveCharacterTextSplitter
from utils.logger import logger


class DocumentChunker:
    """Split documents into chunks for embedding"""

    def __init__(
        self,
        chunk_size: int = 2000,
        chunk_overlap: int = 400
    ):
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=len,
            separators=["\n\n", "\n", ". ", " ", ""]
        )
        logger.info(f"Initialized chunker: size={chunk_size}, overlap={chunk_overlap}")

    def chunk_documents(
        self,
        documents: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Split documents into chunks

        Args:
            documents: List of dicts with 'content' and 'metadata'

        Returns:
            List of chunks with inherited metadata
        """
        all_chunks = []

        for doc in documents:
            content = doc["content"]
            metadata = doc["metadata"]

            # Split the content
            chunks = self.text_splitter.split_text(content)

            # Create chunk documents with metadata
            for i, chunk_text in enumerate(chunks):
                chunk_metadata = metadata.copy()
                chunk_metadata["chunk_index"] = i
                chunk_metadata["total_chunks"] = len(chunks)

                all_chunks.append({
                    "content": chunk_text,
                    "metadata": chunk_metadata
                })

        logger.info(f"Created {len(all_chunks)} chunks from {len(documents)} documents")
        return all_chunks
