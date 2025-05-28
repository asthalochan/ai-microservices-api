"""
main.py
Entry-point for the AI Microservices Gateway (FastAPI).
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum

# ------------------------------------------------------------------------------
# Environment & configuration
# ------------------------------------------------------------------------------

# Load .env only when NOT running inside a Lambda container
if os.getenv("AWS_LAMBDA_FUNCTION_NAME") is None:
    # Look for .env in the project root
    env_file = Path(__file__).parent / ".env"
    load_dotenv(dotenv_path=env_file, override=False)

# Validate critical env var
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise RuntimeError(
        "Environment variable OPENAI_API_KEY is missing! "
        "Add it to your deployment settings or to a local .env file."
    )

# ------------------------------------------------------------------------------
# FastAPI application
# ------------------------------------------------------------------------------

app = FastAPI(
    title="AI Microservices Gateway",
    version="1.0.0",
    description="Central API for AI-powered tools such as the Article Writer",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS — allow everything for now (tighten in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # e.g. ["https://your-frontend.com"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
from apps.ai_article_writer.routes import router as article_writer_router  # noqa: E402

app.include_router(article_writer_router, prefix="/article-writer", tags=["Article Writer"])

# ------------------------------------------------------------------------------
# Health/root route
# ------------------------------------------------------------------------------

@app.get("/", tags=["Health"])
async def root() -> dict:
    """Basic health check."""
    return {
        "message": "Welcome to the AI Microservices API",
        "endpoints": {
            "Article Writer": "/article-writer/write-article",
        },
        "status": "online",
    }

# ------------------------------------------------------------------------------
# Lambda handler (only used if deployed to AWS Lambda)
# ------------------------------------------------------------------------------

handler = Mangum(app)

# ------------------------------------------------------------------------------
# Local development entry-point
# ------------------------------------------------------------------------------

if __name__ == "__main__":
    import uvicorn

    # Use PORT env var if provided (Render sets PORT=10000)
    port = int(os.getenv("PORT", 8000))

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
