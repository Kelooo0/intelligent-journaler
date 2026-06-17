from google import genai
from google.genai import types
from loguru import logger

from app.schemas.schemas import EntryAnalysis


class AIService:
    def __init__(self) -> None:
        logger.debug("Initializing genai client")
        self.client = genai.Client().aio
        self.model_id = "gemini-2.5-flash"
        self.embedding_model = "gemini-embedding-001"

    async def analyze_entry(self, content: str, tags: str) -> EntryAnalysis:
        logger.info("Analyzing entry content")
        try:
            logger.debug("Creating prompt")
            prompt = f"""
                Content: {content}
                Available existing tags: {tags}

                TASK:
                Analyze the journal entry provided in 'Content'.

                LANGUAGE:
                Respond in the same language as the Content.

                RULES FOR TAGS:
                1. Every tag must be a noun in the singular form
                (base form, e.g., "training", "work", "sadness").
                2. Never use plurals, verbs, or inflected forms
                (e.g., DO NOT use "trainings", "working", "sadly").
                3. Write all tags in lowercase.
            """
            logger.debug("Fetching response from ai model")
            response = await self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=EntryAnalysis,
                    temperature=0.1,
                ),
            )
            data = EntryAnalysis.model_validate_json(response.text)
            logger.debug("Returning a validated analysis data")
            return data
        except Exception:
            logger.exception("An AIService error occured")
            return EntryAnalysis()

    async def get_embedding(self, content: str) -> list[float] | None:
        logger.debug("Generating an embedding for provided content")
        try:
            response = await self.client.models.embed_content(
                model=self.embedding_model,
                contents=content,
                config=types.EmbedContentConfig(output_dimensionality=768),
            )
            return response.embeddings[0].values
        except Exception:
            logger.exception("An error occured while generating an embedding")
            return None


ai_service = AIService()
