"""LLM Service - Wrapper for multiple LLM providers"""

import asyncio
import logging
from typing import Optional
from config import settings

# Optional imports for LangChain / providers. Keep service import-safe when
# dependencies aren't installed so tests and basic app functionality work
# without API keys or heavy packages.
try:
    from langchain.chat_models import ChatOpenAI
except Exception:
    ChatOpenAI = None

try:
    # Anthropic chat model may be available under different packages;
    # attempt the most likely import path and fall back to None.
    from langchain.chat_models import ChatAnthropic
except Exception:
    ChatAnthropic = None

try:
    from langchain.schema import HumanMessage, SystemMessage
except Exception:
    # Minimal fallback message classes used only to keep APIs consistent
    class HumanMessage:
        def __init__(self, content: str):
            self.content = content

    class SystemMessage:
        def __init__(self, content: str):
            self.content = content

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with LLMs"""
    
    def __init__(self):
        self.openai_model = None
        self.anthropic_model = None
        self._init_models()
    
    def _init_models(self):
        """Initialize LLM models"""
        # Initialize OpenAI model if package and key are available
        if ChatOpenAI is not None and settings.openai_api_key:
            try:
                self.openai_model = ChatOpenAI(
                    model_name=settings.llm_model,
                    temperature=settings.temperature,
                    api_key=settings.openai_api_key
                )
                logger.info(f"✓ Initialized OpenAI model: {settings.llm_model}")
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI model: {e}")

        # Initialize Anthropic model if package and key are available
        if ChatAnthropic is not None and settings.anthropic_api_key:
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
                return getattr(response, "content", str(response))

            # Prefer OpenAI model when available
            if self.openai_model:
                response = await asyncio.to_thread(self.openai_model.invoke, messages)
                return getattr(response, "content", str(response))

            # No LLM configured; return a safe fallback explanatory text
            logger.warning("No LLM configured — returning fallback response")
            fallback = (
                "[LLM not configured] The system cannot generate a full response because"
                " no LLM provider is configured. Install the provider SDK and set API keys"
                " to enable full functionality."
            )
            return fallback
        except Exception as e:
            logger.error(f"Text generation failed: {e}")
            # Return fallback instead of raising to keep endpoints stable
            return "[LLM error] Text generation failed"
    
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
                if self.openai_model:
                    llm = self.openai_model
                else:
                    # No LLM configured — yield fallback message and exit
                    yield (
                        "[LLM not configured] Streaming not available. Configure an LLM "
                        "provider to stream responses."
                    )
                    return

            # Stream tokens
            for chunk in llm.stream(messages):
                content = getattr(chunk, "content", None)
                if content:
                    yield content
        except Exception as e:
            logger.error(f"Text streaming failed: {e}")
            # Yield a simple error message to keep streams stable
            yield "[LLM error] Text streaming failed"


# Singleton instance
llm_service = LLMService()
