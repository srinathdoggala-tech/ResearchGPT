import logging
from typing import Optional
import google.generativeai as genai

from config import settings

logger = logging.getLogger(__name__)


class LLMService:
    def __init__(self):
        self.model = None
        self._init_model()

    def _init_model(self):
        try:
            if not settings.gemini_api_key:
                logger.warning("No Gemini API key configured")
                return

            genai.configure(api_key=settings.gemini_api_key)

            model_name = settings.llm_model or "gemini-1.5-flash"

            self.model = genai.GenerativeModel(model_name)

            logger.info(f"✓ Gemini initialized: {model_name}")

        except Exception as e:
            logger.error(f"Gemini initialization failed: {e}")

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: str = "gemini",
    ) -> str:

        try:
            if not self.model:
                return "[Gemini not configured]"

            final_prompt = prompt

            if system_prompt:
                final_prompt = f"{system_prompt}\n\n{prompt}"

            response = self.model.generate_content(final_prompt)

            return response.text

        except Exception as e:
            logger.error(f"Gemini generation failed: {e}")
            return f"[LLM ERROR]\n{str(e)}"

    async def stream_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: str = "gemini",
    ):
        try:
            if not self.model:
                yield "[Gemini not configured]"
                return

            final_prompt = prompt

            if system_prompt:
                final_prompt = f"{system_prompt}\n\n{prompt}"

            response = self.model.generate_content(
                final_prompt,
                stream=True
            )

            for chunk in response:
                if hasattr(chunk, "text") and chunk.text:
                    yield chunk.text

        except Exception as e:
            yield f"[STREAM ERROR] {str(e)}"


llm_service = LLMService()