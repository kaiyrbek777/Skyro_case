"""
Configuration management using Pydantic Settings
"""
from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # Database
    database_url: str = "postgresql://skyro:skyro_secure_pass@postgres:5432/skyro_knowledge"

    # OpenAI
    openai_api_key: str

    # Optional: Anthropic
    anthropic_api_key: Optional[str] = None

    # Embeddings
    embedding_model: str = "text-embedding-3-small"
    embedding_dimension: int = 1536

    # LLM
    llm_provider: str = "openai"
    llm_model: str = "gpt-4o"
    llm_temperature: float = 0.1
    llm_max_tokens: int = 2000

    # Application
    environment: str = "development"
    log_level: str = "INFO"
    auto_ingest_on_startup: bool = True
    clear_db_before_ingestion: bool = True  # Clear existing chunks before re-indexing

    # Retrieval
    retrieval_top_k: int = 5
    retrieval_similarity_threshold: float = 0.2
    use_parent_document_retrieval: bool = True  # Retrieve all chunks from matched sources

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Global settings instance
settings = Settings()
