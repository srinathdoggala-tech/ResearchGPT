import logging
import asyncio
import os
from typing import Optional, AsyncGenerator

import google.generativeai as genai

from config import settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.model = None
        self.model_name = None
        self._init_model()

    def _init_model(self):
        try:
            api_key = settings.gemini_api_key or os.getenv("GEMINI_API_KEY")

            if not api_key:
                logger.warning("No Gemini API key configured")
                return

            genai.configure(api_key=api_key)

            # Force a supported model
            self.model_name = (
                os.getenv("LLM_MODEL")
                or getattr(settings, "llm_model", None)
                or "gemini-2.5-flash"
            )

            logger.info(f"Attempting Gemini model: {self.model_name}")

            self.model = genai.GenerativeModel(self.model_name)

            logger.info(
                f"✓ Gemini initialized successfully: {self.model_name}"
            )

        except Exception as e:
            logger.error(f"Gemini initialization failed: {e}")
            self.model = None

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: str = "gemini",
    ) -> str:

        if not self.model:
            self._init_model()

        if not self.model:
            return "[Gemini not configured properly]"

        final_prompt = (
            f"{system_prompt}\n\n{prompt}"
            if system_prompt
            else prompt
        )

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                final_prompt
            )

            if hasattr(response, "text") and response.text:
                return response.text

            return "[No text response generated]"

        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            return f"[LLM ERROR] {str(e)}"

    async def stream_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: str = "gemini",
    ) -> AsyncGenerator[str, None]:

        if not self.model:
            self._init_model()

        if not self.model:
            yield "[Gemini initialization failed]"
            return

        final_prompt = (
            f"{system_prompt}\n\n{prompt}"
            if system_prompt
            else prompt
        )

        try:
            response = await asyncio.to_thread(
                self.model.generate_content,
                final_prompt,
                stream=True
            )

            for chunk in response:
                if hasattr(chunk, "text") and chunk.text:
                    yield chunk.text
                    await asyncio.sleep(0.01)

        except Exception as e:
            logger.error(f"Streaming failed: {e}")
            yield f"[STREAM ERROR] {str(e)}"


llm_service = LLMService()