"""
Generate embeddings using OpenAI API
"""
from typing import List
from openai import OpenAI
from config import settings
from utils.logger import logger


class Embedder:
    """Generate embeddings for text chunks"""

    def __init__(self):
        self.client = OpenAI(api_key=settings.openai_api_key)
        self.model = settings.embedding_model
        logger.info(f"Initialized embedder with model: {self.model}")

    def embed_texts(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for a list of texts

        Args:
            texts: List of text strings

        Returns:
            List of embedding vectors
        """
        if not texts:
            return []

        try:
            # OpenAI allows batching up to 2048 texts
            batch_size = 100
            all_embeddings = []

            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]

                response = self.client.embeddings.create(
                    model=self.model,
                    input=batch
                )

                embeddings = [item.embedding for item in response.data]
                all_embeddings.extend(embeddings)

                logger.debug(f"Generated embeddings for batch {i//batch_size + 1}")

            logger.info(f"Generated {len(all_embeddings)} embeddings")
            return all_embeddings

        except Exception as e:
            logger.error(f"Failed to generate embeddings: {e}")
            raise

    def embed_query(self, query: str) -> List[float]:
        """
        Generate embedding for a single query

        Args:
            query: Query text

        Returns:
            Embedding vector
        """
        try:
            response = self.client.embeddings.create(
                model=self.model,
                input=query
            )
            return response.data[0].embedding

        except Exception as e:
            logger.error(f"Failed to embed query: {e}")
            raise
