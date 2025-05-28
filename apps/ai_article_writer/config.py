# apps/ai_article_writer/config.py

from pydantic_settings  import BaseSettings
from dotenv import load_dotenv
import os

# Load .env only outside AWS Lambda
if os.getenv("OPENAI_API_KEY") is None:
    load_dotenv()

class Settings(BaseSettings):
    app_name: str = "AI Article Writer"
    openai_api_key: str
    model_name: str = "gpt-4o"
    temperature: float = 0.7
    debug: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
