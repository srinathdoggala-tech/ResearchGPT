"""
ResearchGPT FastAPI Application
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from config import settings
from api.routes import router

# Logging

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

```
yield

logger.info("👋 Shutting down ResearchGPT API")
```

app = FastAPI(
title="ResearchGPT API",
description="Multi-Agent AI Research Assistant",
version="1.0.0",
lifespan=lifespan,
)

# CORS

app.add_middleware(
CORSMiddleware,
allow_origins=["*"],
allow_credentials=True,
allow_methods=["*"],
allow_headers=["*"],
)

# API Routes

app.include_router(router)

@app.get("/")
async def root():
return {
"message": "ResearchGPT API Running",
"version": "1.0.0",
"docs": "/docs",
"health": "/health",
}

@app.get("/health")
async def health():
return {
"status": "healthy",
"service": "ResearchGPT",
"version": "1.0.0",
}

# Required for Vercel

application = app

if **name** == "**main**":
import uvicorn

```
uvicorn.run(
    "main:app",
    host="0.0.0.0",
    port=8000,
    reload=True,
)
```
