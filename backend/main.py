"""
Main FastAPI application entry point
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes import router, initialize_workflow
from config import settings
from utils.logger import logger
from ingestion.ingest_pipeline import run_ingestion
import time


# Create FastAPI app
app = FastAPI(
    title="Skyro Knowledge Assistant API",
    description="AI-powered internal knowledge access using RAG",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routes
app.include_router(router)


@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("=" * 60)
    logger.info("Starting Skyro Knowledge Assistant")
    logger.info("=" * 60)
    logger.info(f"Environment: {settings.environment}")
    logger.info(f"LLM Provider: {settings.llm_provider}")
    logger.info(f"LLM Model: {settings.llm_model}")
    logger.info(f"Embedding Model: {settings.embedding_model}")

    # Wait for database to be ready
    logger.info("Waiting for database to be ready...")
    time.sleep(5)

    # Run ingestion if enabled
    if settings.auto_ingest_on_startup:
        logger.info("Auto-ingestion enabled, running ingestion pipeline...")
        try:
            run_ingestion()
        except Exception as e:
            logger.error(f"Ingestion failed: {e}")
            logger.info("Continuing with existing data...")

    # Initialize RAG workflow
    logger.info("Initializing RAG workflow...")
    initialize_workflow()

    logger.info("=" * 60)
    logger.info("✓ Skyro Knowledge Assistant is ready!")
    logger.info("API docs available at: http://localhost:8000/docs")
    logger.info("=" * 60)


@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Shutting down Skyro Knowledge Assistant")


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.environment == "development"
    )
