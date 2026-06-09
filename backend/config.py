from pydantic_settings import BaseSettings
from typing import List
import logging


class Settings(BaseSettings):
    """Application settings"""

    # API Keys
    gemini_api_key: str = ""
    tavily_api_key: str = ""

    # Optional Providers
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # LLM Configuration
    llm_model: str = "gemini-2.5-flash"
    temperature: float = 0.7

    # Search
    search_max_results: int = 5

    # Server
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 1

    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # Database
    database_url: str = "sqlite:///./research.db"

    # Logging
    log_level: str = "INFO"

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
        "extra": "ignore",
    }


settings = Settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)