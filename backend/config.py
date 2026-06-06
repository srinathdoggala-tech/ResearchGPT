try:
    from pydantic_settings import BaseSettings
except Exception:
    # Fall back to pydantic's BaseSettings for older/newer installs
    try:
        from pydantic import BaseSettings
    except Exception:
        # Minimal fallback if pydantic isn't installed; provides defaults only
        class BaseSettings:
            def __init__(self, **kwargs):
                pass
from typing import List
import logging


class Settings(BaseSettings):
    """Application settings"""
    
    # LLM Configuration
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    llm_model: str = "gpt-4"
    temperature: float = 0.7
    
    # Search Configuration
    tavily_api_key: str = ""
    search_max_results: int = 5
    
    # Server Configuration
    debug: bool = True
    host: str = "0.0.0.0"
    port: int = 8000
    workers: int = 4
    
    # CORS Configuration
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:5173"]
    
    # Database Configuration
    database_url: str = "sqlite:///./research.db"
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


settings = Settings()

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.log_level),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)
