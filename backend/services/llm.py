import logging
import asyncio
from typing import Optional, AsyncGenerator
import google.generativeai as genai
from config import settings

logger = logging.getLogger(__name__)

class LLMService:
    def __init__(self):
        self.model = None
        self._init_model()

    def _init_model(self):
        try:
            # Check config fallback strategies for serverless environments
            api_key = settings.gemini_api_key or os.getenv("GEMINI_API_KEY")
            if not api_key:
                logger.warning("No Gemini API key configured in execution context")
                return

            genai.configure(api_key=api_key)
            model_name = settings.llm_model or "gemini-1.5-flash"
            self.model = genai.GenerativeModel(model_name)
            logger.info(f"✓ Gemini initialized successfully: {model_name}")
        except Exception as e:
            logger.error(f"Gemini initialization failed: {e}")

    async def generate_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: str = "gemini",
    ) -> str:
        if not self.model:
            self._init_model()
            if not self.model:
                return "[Gemini not configured properly in production environment]"

        final_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt
        max_retries = 3

        for attempt in range(max_retries):
            try:
                # Execute blocking SDK network operations within an isolated worker thread pool
                response = await asyncio.to_thread(self.model.generate_content, final_prompt)
                if hasattr(response, "text"):
                    return response.text
                return "[No text response payload generated]"
            except Exception as e:
                error_msg = str(e)
                logger.error(f"Gemini error (Attempt {attempt + 1}/{max_retries}): {error_msg}")
                
                if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                    if attempt < max_retries - 1:
                        # Adaptive linear backoff duration matching serverless scales
                        await asyncio.sleep(5 * (attempt + 1))
                        continue
                    return "AI Generation rate limits reached. Please retry shortly."
                return f"[LLM GENERATION ERROR]: {error_msg}"
        return "[LLM ERROR] Retry thresholds exhausted."

    async def stream_text(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: str = "gemini",
    ) -> AsyncGenerator[str, None]:
        if not self.model:
            self._init_model()
            if not self.model:
                yield "[Gemini initialization failure]"
                return

        final_prompt = f"{system_prompt}\n\n{prompt}" if system_prompt else prompt

        try:
            # Trigger standard streaming call in an isolated thread
            response = await asyncio.to_thread(
                self.model.generate_content, final_prompt, stream=True
            )
            
            # Unroll chunks iteratively without locking up the master async loop
            for chunk in response:
                if hasattr(chunk, "text") and chunk.text:
                    yield chunk.text
                    # Small yield slice to give control back to serverless IO multiplexer
                    await asyncio.sleep(0.01)
        except Exception as e:
            logger.error(f"Asynchronous Stream failure: {e}")
            yield f"[RUNTIME STREAM ERROR]: {str(e)}"