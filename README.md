# Skyro AI Knowledge Assistant

AI-powered internal knowledge access system built with LangGraph, pgvector, and OpenAI.

## Overview

A production-ready RAG (Retrieval-Augmented Generation) system designed to help employees quickly find information across internal documents.

**Key Features:**
- Semantic search using pgvector with HNSW indexing
- LangGraph workflow orchestration
- Multi-format document support (Markdown, TXT, JSON, PDF)
- Interactive chat interface
- Source attribution and feedback system

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────┐
│                    User Interface                        │
│              Streamlit Chat UI (Port 8501)              │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                    Backend API                           │
│              FastAPI Server (Port 8000)                 │
│                                                          │
│  ┌────────────────────────────────────────────────┐    │
│  │            LangGraph Workflow                  │    │
│  │  Retrieve → Evaluate → Format → Generate      │    │
│  └────────────────────────────────────────────────┘    │
└───────────────────────┬─────────────────────────────────┘
                        │
                        ▼
┌─────────────────────────────────────────────────────────┐
│                 Vector Database                          │
│              PostgreSQL + pgvector                      │
│  ┌──────────────────────────────────────────────┐      │
│  │  Documents Table                             │      │
│  │  ├─ content (text)                           │      │
│  │  ├─ embedding (vector[1536])                 │      │
│  │  ├─ metadata (jsonb)                         │      │
│  │  └─ HNSW Index                               │      │
│  └──────────────────────────────────────────────┘      │
└─────────────────────────────────────────────────────────┘
```

### Technology Stack

| Component | Technology |
|-----------|-----------|
| Workflow Orchestration | LangGraph |
| Vector Database | PostgreSQL + pgvector |
| Embeddings | OpenAI text-embedding-3-small (1536-dim) |
| LLM | OpenAI GPT-4o |
| Backend API | FastAPI |
| Frontend | Streamlit |
| Container Orchestration | Docker Compose |
| Language | Python 3.11 |

## Quick Start

### Prerequisites

- Docker and Docker Compose installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/kaiyrbek777/Skyro_case.git
cd Skyro_case
```

2. **Configure environment variables**
```bash
cp .env.example .env
nano .env  # Add your OPENAI_API_KEY
```

Required:
```
OPENAI_API_KEY=sk-your-key-here
```

3. **Start services**
```bash
docker-compose up -d
```

This will:
- Start PostgreSQL with pgvector extension
- Initialize database schema
- Start backend API server
- Ingest sample documents automatically
- Start Streamlit web interface

4. **Access the application**

Web UI: http://localhost:8501
API Docs: http://localhost:8000/docs
Health Check: http://localhost:8000/health

## Project Structure

```
skyro-knowledge-assistant/
├── docker-compose.yml
├── .env.example
├── README.md
│
├── database/
│   └── init.sql                 # PostgreSQL schema
│
├── data/
│   └── documents/               # Sample documents
│       ├── confluence/          # Wiki docs
│       ├── meetings/            # Meeting notes
│       └── product_specs/       # Product specifications
│
├── backend/
│   ├── main.py                  # FastAPI application
│   ├── config.py                # Configuration
│   │
│   ├── ingestion/               # Document processing
│   │   ├── document_loader.py
│   │   ├── chunker.py
│   │   ├── embedder.py
│   │   └── ingest_pipeline.py
│   │
│   ├── vector_store/
│   │   └── pgvector_store.py    # Vector operations
│   │
│   ├── graph/                   # LangGraph workflow
│   │   ├── state.py
│   │   ├── nodes.py
│   │   └── workflow.py
│   │
│   └── api/
│       ├── models.py
│       └── routes.py
│
└── frontend/
    ├── app.py                   # Streamlit application
    └── utils/
        └── api_client.py
```

## How It Works

### Document Ingestion

```
Documents → Load → Chunk (2000 chars, 400 overlap)
         → Embed (OpenAI) → Store in pgvector
```

### Query Processing

```
User Question → Embed → Vector Search → Retrieve Top-K
             → LangGraph Workflow → Generate Answer
```

### LangGraph Workflow

1. **Retrieve Documents**: Semantic search in pgvector (top-5)
2. **Evaluate Context**: Check relevance scores
3. **Format Context**: Structure documents for LLM
4. **Generate Answer**: GPT-4o generates response with sources

## Configuration

### Environment Variables

```bash
# Required
OPENAI_API_KEY=sk-...

# Optional - Database
DATABASE_URL=postgresql://skyro:skyro_secure_pass@postgres:5432/skyro_knowledge

# Optional - Models
EMBEDDING_MODEL=text-embedding-3-small
LLM_MODEL=gpt-4o
LLM_TEMPERATURE=0.1
```

### Backend Settings

Located in `backend/config.py`:

- `chunk_size`: 2000 characters
- `chunk_overlap`: 400 characters
- `retrieval_top_k`: 5 documents
- `retrieval_similarity_threshold`: 0.2
- `clear_db_before_ingestion`: True

## Adding Documents

### Supported Formats

- Markdown (.md)
- Plain Text (.txt)
- JSON (.json)
- PDF (.pdf)

### Steps

1. Place files in `data/documents/` subdirectories:
   - `confluence/` - Wiki pages
   - `meetings/` - Meeting notes
   - `product_specs/` - Technical specs

2. Restart backend:
```bash
docker-compose restart backend
```

3. Wait for ingestion (check logs):
```bash
docker-compose logs -f backend
```

4. Documents are now searchable via the UI

## API Reference

### Query Endpoint

```bash
POST /api/v1/query
Content-Type: application/json

{
  "question": "What are the API rate limits?"
}

Response:
{
  "question": "What are the API rate limits?",
  "answer": "...",
  "sources": [
    {
      "source": "api-rate-limiting-policy.md",
      "type": "confluence",
      "relevance": "0.89"
    }
  ]
}
```

### Health Check

```bash
GET /health

Response:
{
  "status": "healthy",
  "database_connected": true,
  "total_documents": 66,
  "unique_documents": 14,
  "document_types": {
    "confluence": {"documents": 7, "chunks": 30},
    "product_specs": {"documents": 4, "chunks": 22},
    "meetings": {"documents": 3, "chunks": 14}
  }
}
```

### Feedback Endpoint

```bash
POST /api/v1/feedback

{
  "query": "...",
  "answer": "...",
  "helpful": true,
  "comment": "Great answer!"
}
```

## Scaling Considerations

### Performance Optimization

- Use database read replicas for vector search
- Implement caching layer (Redis) for frequent queries
- Batch embedding generation during ingestion
- Add connection pooling for database

### Deployment

- Kubernetes for auto-scaling
- Managed PostgreSQL with pgvector (AWS RDS, GCP Cloud SQL)
- Load balancing (NGINX, Kong)
- CDN for frontend assets

### Monitoring

- Prometheus + Grafana for metrics
- ELK stack for centralized logging
- Sentry for error tracking
- Track: query latency, retrieval accuracy, LLM costs

### Security

- Implement RBAC (role-based access control)
- Add document-level permissions
- API authentication (OAuth 2.0)
- Rate limiting per user
- Audit logging

## Design Decisions

### LangGraph

**Advantages:**
- Explicit workflow control
- Easy debugging and tracing
- Conditional logic support
- Production-ready framework

**Trade-off:** Newer framework with smaller community

### pgvector

**Advantages:**
- PostgreSQL extension (ACID transactions)
- SQL + vector search in one database
- Cost-effective
- Production-ready

**Trade-off:** Slower than specialized vector databases (Pinecone, Weaviate)

### OpenAI

**Advantages:**
- High-quality embeddings and LLM
- Fast response times
- Simple API

**Trade-offs:**
- Cost at scale
- Data sent to third-party

**Mitigation:** Can swap to open-source models (Llama 3, Mistral) for cost/privacy

## Troubleshooting

### Backend fails to start

```bash
docker-compose logs backend
docker-compose restart backend
```

### No documents indexed

```bash
# Check health
curl http://localhost:8000/health

# Manually trigger ingestion
docker-compose exec backend python -c "from ingestion.ingest_pipeline import run_ingestion; run_ingestion()"
```

### Slow queries

```bash
# Verify HNSW index exists
docker-compose exec postgres psql -U skyro -d skyro_knowledge -c "\d documents"
```

### Database connection issues

```bash
# Restart database
docker-compose restart postgres

# Check database logs
docker-compose logs postgres
```

## Development

### Running Tests

```bash
cd backend
pytest tests/
```

### Local Development (without Docker)

```bash
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload

# Frontend
cd frontend
pip install -r requirements.txt
streamlit run app.py
```

### Code Style

- Python: PEP 8
- Type hints: Python 3.11+
- Docstrings: Google style

## License

This project is for internal use and evaluation purposes.

## Contact

For questions or support, please contact the engineering team.
