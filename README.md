# Skyro AI Knowledge Assistant 🧠

**AI-Powered Internal Knowledge Access System**

A production-ready RAG (Retrieval-Augmented Generation) system built with **LangGraph**, **pgvector**, and **OpenAI** to help fintech employees quickly find information across internal documents.

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Features](#features)
- [Technology Stack](#technology-stack)
- [Quick Start](#quick-start)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Example Questions](#example-questions)
- [Scaling to Production](#scaling-to-production)
- [Integration Examples](#integration-examples)
- [Team Rollout Strategy](#team-rollout-strategy)
- [Design Decisions & Trade-offs](#design-decisions--trade-offs)
- [Future Enhancements](#future-enhancements)
- [Troubleshooting](#troubleshooting)

---

## Overview

Skyro is exploring how to improve internal knowledge access using AI. This prototype demonstrates an AI-powered assistant that:

- 📚 **Indexes internal documents** (Confluence, meetings, product specs)
- 🔍 **Retrieves relevant context** using semantic search (pgvector)
- 🤖 **Generates accurate answers** using LLMs (OpenAI GPT-4)
- 📊 **Tracks user feedback** to improve over time
- 🚀 **Runs out-of-the-box** with Docker Compose

**Key Metrics:**
- **15 sample documents** covering fintech use cases
- **Sub-second search** with pgvector HNSW indexing
- **High retrieval accuracy** with semantic search
- **100% automated ingestion** on startup

---

## Architecture

### System Architecture Diagram

```
┌──────────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                              │
│                   Streamlit Chat UI (Port 8501)                      │
└────────────────────────────┬─────────────────────────────────────────┘
                             │ HTTP
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                        BACKEND API                                   │
│                  FastAPI Server (Port 8000)                          │
│                                                                      │
│  ┌────────────────────────────────────────────────────────────┐    │
│  │                 LangGraph Workflow                         │    │
│  │                                                            │    │
│  │  ┌──────────────┐      ┌──────────────┐                  │    │
│  │  │   Retrieve   │  →   │   Evaluate   │                  │    │
│  │  │  Documents   │      │   Context    │                  │    │
│  │  └──────────────┘      └──────────────┘                  │    │
│  │         │                      │                          │    │
│  │         ▼                      ▼                          │    │
│  │  ┌──────────────┐      ┌──────────────┐                  │    │
│  │  │   Format     │  →   │   Generate   │                  │    │
│  │  │   Context    │      │    Answer    │                  │    │
│  │  └──────────────┘      └──────────────┘                  │    │
│  └────────────────────────────────────────────────────────────┘    │
└────────────────────────────┬─────────────────────────────────────────┘
                             │
                             ▼
┌──────────────────────────────────────────────────────────────────────┐
│                    VECTOR DATABASE                                   │
│                PostgreSQL + pgvector                                 │
│                                                                      │
│  ┌─────────────────────────────────────────────────────────┐       │
│  │  Documents Table                                        │       │
│  │  ├─ content (text)                                      │       │
│  │  ├─ embedding (vector[1536])                            │       │
│  │  ├─ metadata (jsonb)                                    │       │
│  │  └─ HNSW Index for fast similarity search              │       │
│  └─────────────────────────────────────────────────────────┘       │
└──────────────────────────────────────────────────────────────────────┘
                             ▲
                             │
                  ┌──────────┴──────────┐
                  │                     │
         ┌────────▼────────┐   ┌───────▼────────┐
         │  OpenAI API     │   │  Document      │
         │  Embeddings     │   │  Ingestion     │
         │  (startup)      │   │  Pipeline      │
         └─────────────────┘   └────────────────┘
```

### Data Flow

```
1. INGESTION (Startup)
   Document Files → DocumentLoader → Chunker → Embedder → pgvector

2. QUERY (Runtime)
   User Question → Embed Query → Vector Search → Retrieve Top-K Docs
   → LangGraph (Evaluate + Format + Generate) → Return Answer + Sources

3. FEEDBACK (Optional)
   User Rating → Store in feedback table → Future improvements
```

---

## Features

### Core Functionality
✅ **RAG Pipeline** with LangGraph for orchestration
✅ **Vector Search** using pgvector (HNSW indexing)
✅ **Semantic Embeddings** via OpenAI `text-embedding-3-small`
✅ **LLM Generation** via OpenAI GPT-4-turbo
✅ **Multi-Format Support** - Markdown, TXT, JSON, **PDF** documents
✅ **Automatic Document Ingestion** on container startup
✅ **Interactive Chat UI** with Streamlit
✅ **Source Attribution** - shows which documents were used
✅ **Feedback System** - thumbs up/down for answers
✅ **Health Monitoring** - API health checks and metrics

### Technical Highlights
- **Modular Design** - Easy to swap LLM providers or vector stores
- **Production-Ready** - Docker Compose, health checks, logging
- **Scalable** - Async processing, connection pooling
- **Secure** - Environment variables, input validation
- **Observable** - Structured logging, metrics

---

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Orchestration** | LangGraph | RAG workflow management |
| **Vector DB** | pgvector (PostgreSQL) | Semantic search & storage |
| **Embeddings** | OpenAI text-embedding-3-small | Document & query vectorization |
| **LLM** | OpenAI GPT-4-turbo | Answer generation |
| **Backend** | FastAPI | REST API server |
| **Frontend** | Streamlit | Interactive chat UI |
| **Container** | Docker Compose | Local development & deployment |
| **Language** | Python 3.11 | Primary programming language |

---

## Quick Start

### Prerequisites
- Docker & Docker Compose installed
- OpenAI API key ([Get one here](https://platform.openai.com/api-keys))

**📖 New to this? Check out [SETUP_GUIDE.md](SETUP_GUIDE.md) for step-by-step beginner instructions!**

### 1. Clone the Repository
```bash
git clone https://github.com/kaiyrbek777/Skyro_case.git
cd Skyro_case
```

### 2. Configure Environment Variables
```bash
cp .env.example .env
nano .env  # Add your OPENAI_API_KEY
```

**Required Configuration:**
```bash
OPENAI_API_KEY=sk-your-key-here
```

### 3. Start All Services
```bash
docker-compose up -d
```

**This will:**
1. Start PostgreSQL with pgvector extension
2. Initialize database schema
3. Start backend (FastAPI)
4. Automatically ingest 15 sample documents
5. Start frontend (Streamlit UI)

### 4. Access the Application

**Web UI:**
```
http://localhost:8501
```

**API Documentation:**
```
http://localhost:8000/docs
```

**Health Check:**
```bash
curl http://localhost:8000/health
```

### 5. Try Example Questions

Ask questions like:
- "What are our Q1 2024 OKRs?"
- "How does our fraud detection system work?"
- "What are the API rate limits?"
- "Tell me about the customer onboarding flow"

---

## Project Structure

```
skyro-knowledge-assistant/
├── docker-compose.yml           # Container orchestration
├── .env.example                 # Environment template
├── README.md                    # This file
│
├── database/
│   └── init.sql                 # PostgreSQL schema & pgvector setup
│
├── data/
│   └── documents/               # Sample fintech documents (15 total)
│       ├── confluence/          # Internal wiki docs (6 files)
│       ├── meetings/            # Meeting notes (3 files)
│       └── product_specs/       # Product specifications (6 files)
│
├── backend/                     # FastAPI + LangGraph backend
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── main.py                  # FastAPI application entry
│   ├── config.py                # Settings management
│   │
│   ├── ingestion/               # Document processing pipeline
│   │   ├── document_loader.py   # Load various file formats
│   │   ├── chunker.py           # Split documents into chunks
│   │   ├── embedder.py          # Generate OpenAI embeddings
│   │   └── ingest_pipeline.py   # Orchestrate ingestion
│   │
│   ├── vector_store/            # pgvector integration
│   │   └── pgvector_store.py    # Vector search & storage
│   │
│   ├── graph/                   # LangGraph RAG workflow
│   │   ├── state.py             # Graph state definition
│   │   ├── nodes.py             # Workflow nodes
│   │   └── workflow.py          # Graph assembly
│   │
│   ├── api/                     # REST API
│   │   ├── models.py            # Pydantic request/response models
│   │   └── routes.py            # API endpoints
│   │
│   └── utils/
│       └── logger.py            # Logging configuration
│
└── frontend/                    # Streamlit chat UI
    ├── Dockerfile
    ├── requirements.txt
    ├── app.py                   # Main Streamlit application
    └── utils/
        └── api_client.py        # Backend API client
```

---

## How It Works

### 1. Document Ingestion (Startup)

```python
# Automatic process when backend starts
DocumentLoader().load_all_documents()
  → DocumentChunker().chunk_documents()  # 800 char chunks, 200 overlap
  → Embedder().embed_texts()             # OpenAI text-embedding-3-small
  → PgVectorStore().add_documents()      # Store in PostgreSQL
```

**Result:** 15 documents → ~127 chunks → Indexed in pgvector

### 2. Query Processing (Runtime)

```python
# LangGraph workflow execution
User Question
  → retrieve_documents()          # Vector similarity search
  → evaluate_context()            # Check if context is sufficient
  → format_context()              # Prepare context for LLM
  → generate_answer()             # GPT-4 generates response
  → Return {answer, sources}
```

### 3. LangGraph Workflow Details

**Node 1: Retrieve Documents**
- Embed user query with OpenAI
- Perform cosine similarity search in pgvector
- Return top-5 most relevant chunks

**Node 2: Evaluate Context**
- Check average similarity score
- Determine if context is sufficient (threshold: 0.75)
- Can trigger query reformulation (simplified in v1.0)

**Node 3: Format Context**
- Combine retrieved chunks
- Add metadata (source, type, relevance)
- Structure for LLM consumption

**Node 4: Generate Answer**
- Send context + question to GPT-4
- System prompt: Act as Skyro internal assistant
- Return answer with source citations

---

## Example Questions

The system can answer questions across various categories:

### Strategy & Planning
- "What are our Q1 2024 OKRs for the growth team?"
- "What features are planned for Q2 2024 roadmap?"

### Technical Documentation
- "How does our payment gateway integration work?"
- "What are the API rate limiting policies?"
- "Explain our fraud detection system architecture"

### Processes & Workflows
- "What is the customer onboarding flow?"
- "How do we handle KYC/AML compliance?"
- "What happened in the security incident postmortem?"

### Product Features
- "What features are in the mobile app?"
- "How does the savings account product work?"

### Operational
- "What is our infrastructure architecture?"
- "How do we run A/B tests?"

---

## Scaling to Production

### Architecture Changes Needed

**1. Scalability**
```
Current:  Single container backend
Future:   Kubernetes deployment with auto-scaling

- Horizontal scaling: 10-100 backend pods
- Load balancer: NGINX or Kong API Gateway
- pgvector: Use managed service (AWS RDS with pgvector)
- Caching layer: Redis for frequent queries
```

**2. Performance Optimization**
```
- Batch embedding generation during ingestion
- Async processing for long-running queries
- CDN for frontend assets
- Database read replicas for search queries
```

**3. Monitoring & Observability**
```
Tools:
- Prometheus + Grafana for metrics
- ELK Stack for centralized logging
- Sentry for error tracking
- OpenTelemetry for distributed tracing

Metrics:
- Query latency (p50, p95, p99)
- Retrieval accuracy
- User feedback scores
- LLM API costs
```

**4. Security Enhancements**
```
- Role-based access control (RBAC)
- Document-level permissions
- Audit logging for all queries
- Rate limiting per user
- API authentication (OAuth 2.0)
```

**5. Cost Optimization**
```
- Use cheaper embeddings for large-scale (e.g., open-source models)
- Cache expensive LLM calls
- Implement tiered LLM routing (GPT-4 for complex, GPT-3.5 for simple)
- Batch processing for non-real-time indexing
```

---

## Integration Examples

### Slack Bot Integration

```python
from slack_bolt import App
from skyro_api_client import SkyroKnowledgeClient

app = App(token=SLACK_BOT_TOKEN)
skyro = SkyroKnowledgeClient(base_url="http://backend:8000")

@app.command("/ask-skyro")
def handle_ask_command(ack, command, respond):
    ack()
    question = command['text']
    result = skyro.query(question)

    blocks = [{
        "type": "section",
        "text": {"type": "mrkdwn", "text": f"*Answer:*\n{result['answer']}"}
    }]

    respond(blocks=blocks)
```

### Web UI Integration (React)

```javascript
import React, { useState } from 'react';
import axios from 'axios';

function KnowledgeSearch() {
  const [question, setQuestion] = useState('');
  const [result, setResult] = useState(null);

  const handleSearch = async () => {
    const response = await axios.post('http://backend:8000/api/v1/query', {
      question: question
    });
    setResult(response.data);
  };

  return (
    <div>
      <input
        value={question}
        onChange={(e) => setQuestion(e.target.value)}
        placeholder="Ask a question..."
      />
      <button onClick={handleSearch}>Search</button>
      {result && <p>{result.answer}</p>}
    </div>
  );
}
```

---

## Team Rollout Strategy

### Phase 1: Internal Alpha (Weeks 1-2)
**Audience:** 10-15 early adopters from engineering & product
**Goal:** Validate core functionality, gather initial feedback

**Activities:**
- Deploy to internal staging environment
- Provide training session (30 min demo)
- Create feedback channel (#skyro-assistant-feedback)
- Track usage metrics & iterate

**Success Criteria:**
- 80% positive feedback
- <5% error rate
- 50+ queries per day

### Phase 2: Private Beta (Weeks 3-6)
**Audience:** 50-100 users across departments
**Goal:** Test scalability, expand document coverage

**Activities:**
- Add more document sources (Jira, GitHub, emails)
- Implement department-specific access controls
- Integrate with Slack (slash command)
- Weekly office hours for Q&A

**Success Criteria:**
- 200+ queries per day
- 70% find answers without escalation
- <2 second average response time

### Phase 3: Company-Wide Rollout (Weeks 7-10)
**Audience:** All employees
**Goal:** Become primary internal knowledge tool

**Activities:**
- Launch announcement (all-hands meeting)
- Department-specific onboarding sessions
- Create help documentation & video tutorials
- 24/7 monitoring & on-call rotation

**Success Criteria:**
- 60% monthly active users
- 1000+ queries per day
- Positive NPS score (>40)
- Reduce support tickets by 30%

---

## Design Decisions & Trade-offs

### Why LangGraph?
**Pros:**
- ✅ Explicit workflow control (no black box)
- ✅ Easy to debug and trace
- ✅ Conditional logic support
- ✅ Built for production (LangChain ecosystem)

**Cons:**
- ❌ Newer framework (smaller community)

**Alternative Considered:** LlamaIndex (more RAG-focused but less flexible)

### Why pgvector?
**Pros:**
- ✅ Production-ready (PostgreSQL extension)
- ✅ ACID transactions
- ✅ SQL + vector search in one DB
- ✅ Cost-effective (no separate vector DB)

**Cons:**
- ❌ Not as fast as specialized vector DBs (Pinecone, Weaviate)

**Alternative Considered:** Pinecone (faster but more expensive, vendor lock-in)

### Why OpenAI?
**Pros:**
- ✅ Best-in-class embeddings & LLM quality
- ✅ Fast response times
- ✅ Simple API

**Cons:**
- ❌ Cost (can be expensive at scale)
- ❌ Data sent to third party (privacy concerns)

**Mitigation:**
- Use open-source models for embeddings (Sentence Transformers)
- Deploy Llama 3 or Mistral for LLM (if privacy is critical)

---

## Future Enhancements

### Short-term (Next 3 months)
- [ ] Multi-language support
- [ ] Document-level access control
- [ ] Advanced filtering (date range, document type)
- [ ] Query history & saved searches
- [ ] Slack & email integrations

### Medium-term (6 months)
- [ ] Hybrid search (keyword + semantic)
- [ ] Re-ranking for better accuracy
- [ ] Summarization for long documents
- [ ] Conversational memory (multi-turn Q&A)
- [ ] Custom embeddings fine-tuning

### Long-term (1 year)
- [ ] Graph-based knowledge representation
- [ ] Automated knowledge base updates
- [ ] Proactive suggestions
- [ ] Multi-modal support (images, videos)
- [ ] Federated search across all company tools

---

## Troubleshooting

### Backend not starting
```bash
# Check logs
docker-compose logs backend

# Common fix:
docker-compose restart backend
```

### No documents indexed
```bash
# Check document count
curl http://localhost:8000/health

# Manually trigger ingestion
docker-compose exec backend python -c "from ingestion.ingest_pipeline import run_ingestion; run_ingestion()"
```

### Slow query responses
```bash
# Check pgvector index
docker-compose exec postgres psql -U skyro -d skyro_knowledge -c "\d documents"
```

---

## Adding Your Own Documents

Want to search through your own documents?

### Supported Formats
- ✅ **Markdown** (.md)
- ✅ **Plain Text** (.txt)
- ✅ **JSON** (.json)
- ✅ **PDF** (.pdf) - automatically extracts text

### How to Add Documents

1. **Place files in the documents folder:**
   ```bash
   # Confluence-style docs
   cp your-doc.md data/documents/confluence/

   # Meeting notes
   cp meeting-notes.pdf data/documents/meetings/

   # Product specs
   cp spec.txt data/documents/product_specs/
   ```

2. **Restart the backend:**
   ```bash
   docker-compose restart backend
   ```

3. **Wait for ingestion** (check logs):
   ```bash
   docker-compose logs -f backend
   # Look for: "✓ Ingestion complete!"
   ```

4. **Start searching!**
   Open http://localhost:8501 and ask questions about your new documents.

**📄 For detailed instructions on adding PDFs and Word docs, see [HOW_TO_ADD_PDF_WORD.md](HOW_TO_ADD_PDF_WORD.md)**

---

## Helpful Guides

- **🚀 [SETUP_GUIDE.md](SETUP_GUIDE.md)** - Step-by-step setup for beginners
- **📄 [HOW_TO_ADD_PDF_WORD.md](HOW_TO_ADD_PDF_WORD.md)** - Guide for adding PDF and Word documents

---

**Built with ❤️ for Skyro Engineering Team**
