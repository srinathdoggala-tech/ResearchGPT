"""LLM Service - Wrapper for multiple LLM providers"""

import asyncio
import logging
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain.schema import HumanMessage, SystemMessage
from config import settings

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with LLMs"""
    
    def __init__(self):
        self.openai_model = None
        self.anthropic_model = None
        self._init_models()
    
    def _init_models(self):
        """Initialize LLM models"""
        if settings.openai_api_key:
            try:
                self.openai_model = ChatOpenAI(
                    model_name=settings.llm_model,
                    temperature=settings.temperature,
                    api_key=settings.openai_api_key
                )
                logger.info(f"✓ Initialized OpenAI model: {settings.llm_model}")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI model: {e}")
        
        if settings.anthropic_api_key:
            try:
                self.anthropic_model = ChatAnthropic(
                    model="claude-3-opus-20240229",
                    temperature=settings.temperature,
                    api_key=settings.anthropic_api_key
                )
                logger.info("✓ Initialized Anthropic model: Claude-3-Opus")
            except Exception as e:
                logger.error(f"Failed to initialize Anthropic model: {e}")
    
    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: str = "openai"
    ) -> str:
        """
        Generate text using specified LLM
        
        Args:
            prompt: User prompt
            system_prompt: System instruction
            model: Model to use (openai or anthropic)
        
        Returns:
            Generated text
        """
        messages = []
        
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        
        messages.append(HumanMessage(content=prompt))
        
        try:
            if model == "anthropic" and self.anthropic_model:
                response = await asyncio.to_thread(self.anthropic_model.invoke, messages)
            else:
                if not self.openai_model:
                    raise ValueError("OpenAI model not initialized")
                response = await asyncio.to_thread(self.openai_model.invoke, messages)
            
            return response.content
        except Exception as e:
            logger.error(f"Text generation failed: {e}")
            raise
    
    async def stream_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: str = "openai"
    ):
        """
        Stream text generation
        
        Args:
            prompt: User prompt
            system_prompt: System instruction
            model: Model to use
        
        Yields:
            Text chunks
        """
        messages = []
        
        if system_prompt:
            messages.append(SystemMessage(content=system_prompt))
        
        messages.append(HumanMessage(content=prompt))
        
        try:
            if model == "anthropic" and self.anthropic_model:
                llm = self.anthropic_model
            else:
                if not self.openai_model:
                    raise ValueError("OpenAI model not initialized")
                llm = self.openai_model
            
            # Stream tokens
            for chunk in llm.stream(messages):
                if chunk.content:
                    yield chunk.content
        except Exception as e:
            logger.error(f"Text streaming failed: {e}")
            raise


# Singleton instance
llm_service = LLMService()
