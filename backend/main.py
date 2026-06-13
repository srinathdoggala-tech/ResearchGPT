"""
ResearchGPT FastAPI Application
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.routes import router

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger("researchgpt")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("🚀 Starting ResearchGPT API")
    logger.info(f"Debug Mode: {settings.debug}")
    logger.info(f"LLM Model: {settings.llm_model}")
    yield
    logger.info("👋 Shutting down ResearchGPT API")

app = FastAPI(
    title="ResearchGPT API",
    description="Multi-Agent AI Research Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

# Robust CORS Configuration for Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Core Multi-Agent Base Router
app.include_router(router, prefix="/api")

@app.get("/")
async def root():
    return {
        "message": "ResearchGPT API Running",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health",
    }

@app.get("/health")
async def health():
    return {
        "status": "healthy",
        "service": "ResearchGPT",
        "version": "1.0.0",
    }

# Vercel Serverless Gateway Hook
application = app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )