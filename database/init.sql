-- ============================================
-- Skyro Knowledge Assistant Database Schema
-- PostgreSQL + pgvector
-- ============================================

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================
-- Documents table with embeddings
-- ============================================
CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    content TEXT NOT NULL,
    metadata JSONB DEFAULT '{}',
    embedding vector(1536),  -- text-embedding-3-small dimension
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Create index for vector similarity search using HNSW
-- HNSW is faster than IVFFlat for most cases
CREATE INDEX IF NOT EXISTS documents_embedding_idx
ON documents USING hnsw (embedding vector_cosine_ops);

-- Create GIN index for JSONB metadata queries
CREATE INDEX IF NOT EXISTS documents_metadata_idx
ON documents USING gin (metadata);

-- Create index for text search
CREATE INDEX IF NOT EXISTS documents_content_idx
ON documents USING gin (to_tsvector('english', content));

-- ============================================
-- Feedback table for user ratings
-- ============================================
CREATE TABLE IF NOT EXISTS feedback (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    answer TEXT NOT NULL,
    helpful BOOLEAN,
    comment TEXT,
    user_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index for analytics queries
CREATE INDEX IF NOT EXISTS feedback_created_at_idx
ON feedback (created_at DESC);

CREATE INDEX IF NOT EXISTS feedback_helpful_idx
ON feedback (helpful);

-- ============================================
-- Query logs table (for analytics)
-- ============================================
CREATE TABLE IF NOT EXISTS query_logs (
    id SERIAL PRIMARY KEY,
    query TEXT NOT NULL,
    retrieved_docs INTEGER,
    response_time_ms INTEGER,
    llm_tokens_used INTEGER,
    user_id VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS query_logs_created_at_idx
ON query_logs (created_at DESC);

-- ============================================
-- Helper function to update updated_at timestamp
-- ============================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER update_documents_updated_at
BEFORE UPDATE ON documents
FOR EACH ROW
EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- Helper function for similarity search
-- ============================================
CREATE OR REPLACE FUNCTION search_documents(
    query_embedding vector(1536),
    match_threshold float DEFAULT 0.7,
    match_count int DEFAULT 5
)
RETURNS TABLE (
    id integer,
    content text,
    metadata jsonb,
    similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        documents.id,
        documents.content,
        documents.metadata,
        1 - (documents.embedding <=> query_embedding) as similarity
    FROM documents
    WHERE 1 - (documents.embedding <=> query_embedding) > match_threshold
    ORDER BY documents.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- ============================================
-- Initial setup complete
-- ============================================
