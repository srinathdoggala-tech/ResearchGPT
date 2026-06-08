import logging
import asyncio
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

            # Recommended free-tier model
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

        if not self.model:
            return "[Gemini not configured]"

        final_prompt = prompt

        if system_prompt:
            final_prompt = f"{system_prompt}\n\n{prompt}"

        max_retries = 3

        for attempt in range(max_retries):
            try:
                response = self.model.generate_content(final_prompt)

                if hasattr(response, "text"):
                    return response.text

                return "[No response generated]"

            except Exception as e:
                error_msg = str(e)

                logger.error(
                    f"Gemini generation failed (attempt {attempt + 1}/{max_retries}): {error_msg}"
                )

                # Handle Gemini quota/rate-limit errors
                if (
                    "429" in error_msg
                    or "quota" in error_msg.lower()
                    or "rate limit" in error_msg.lower()
                ):
                    if attempt < max_retries - 1:
                        wait_time = 20 * (attempt + 1)

                        logger.warning(
                            f"Rate limit hit. Waiting {wait_time}s before retry..."
                        )

                        await asyncio.sleep(wait_time)
                        continue

                    return (
                        "AI quota limit reached. "
                        "Please wait a minute and try again."
                    )

                return f"[LLM ERROR]\n{error_msg}"

        return "[LLM ERROR] Maximum retries exceeded."

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
            logger.error(f"Stream generation failed: {e}")
            yield f"[STREAM ERROR] {str(e)}"


llm_service = LLMService()