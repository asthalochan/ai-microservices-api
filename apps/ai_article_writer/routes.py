# apps/ai_article_writer/routes.py


from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from apps.ai_article_writer.agents_and_logic import run_article_pipeline

router = APIRouter()

class ArticleRequest(BaseModel):
    topic: str

@router.post("/write-article")
async def write_article(request: ArticleRequest):
    topic = request.topic.strip()
    if not topic:
        raise HTTPException(status_code=400, detail="Topic must not be empty.")

    try:
        article_html = run_article_pipeline(topic)
        return {
            "status": "success",
            "topic": topic,
            "article_html": article_html
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate article: {str(e)}")
