import os
import json
import logging
from typing import List, Union
from pydantic_settings import BaseSettings
from pydantic import field_validator


class Settings(BaseSettings):
    """Application settings"""

    # API Keys
    gemini_api_key: str = ""
    tavily_api_key: str = ""

    # Optional Providers
    openai_api_key: str = ""
    anthropic_api_key: str = ""

    # LLM Configuration
    llm_model: str = "gemini-1.5-flash"
    temperature: float = 0.7

    # Search
    search_max_results: int = 5

    # Server
    debug: bool = False
    host: str = "0.0.0.0"
    port: int = 8001
    workers: int = 1

    # CORS - Allow all origins by default for seamless Vercel deployment
    cors_origins: List[str] = ["*"]

    # Database
    database_url: str = "sqlite:///./research.db"

    # Logging
    log_level: str = "INFO"

    @field_validator("debug", mode="before")
    @classmethod
    def parse_debug(cls, v):
        if isinstance(v, str):
            return v.lower() in ("true", "1", "t", "yes", "y", "debug", "development")
        return bool(v)

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            v = v.strip()
            if not v or v == "*":
                return ["*"]
            if v.startswith("[") and v.endswith("]"):
                try:
                    return json.loads(v)
                except Exception:
                    pass
            return [item.strip() for item in v.split(",") if item.strip()]
        return v

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
