from pydantic_settings import BaseSettings
from typing import List
import logging


class Settings(BaseSettings):
    """Application settings"""

    # Gemini Configuration
    gemini_api_key: str = ""

    # Optional (keep if other code still references them)
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    llm_model: str = "gemini-1.5-flash"
    temperature: float = 0.7

    # Search
    tavily_api_key: str = ""
    search_max_results: int = 5

    # Server
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4

    # CORS
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173"
    ]

    # Database
    database_url: str = "sqlite:///./research.db"

    # Logging
    log_level: str = "INFO"

    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)