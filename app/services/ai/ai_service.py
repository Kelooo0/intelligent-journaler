from loguru import logger
from openai import AsyncOpenAI

from app.core.config import settings
from app.schemas.schemas import EntryAnalysis
from app.services.ai.base import AIBase


class AIService(AIBase):
    def __init__(self) -> None:
        self.client = AsyncOpenAI()
        self.model = settings.OPENAI_MODEL
        self.embedding_model = settings.OPENAI_EMBEDDING_MODEL

    async def analyze_entry(self, content: str, tags: str) -> EntryAnalysis:
        logger.info("Analyzing entry content")
        logger.debug("Setting up prompts for analyzing entry content")
        user_prompt = f"""
        Entry content: {content}
        Available existing tags: {tags}
        """
        system_prompt = """
        You analyze personal journal entries and return structured
        data matching the provided schema.

        Use only the journal entry content and the provided list
        of existing tags as sources of truth.

        Rules:

        - Return only data matching the required structured output schema.
        - Do not include explanations, markdown, or additional text.
        - Do not invent events, people, causes, emotions, intentions,
        or conclusions that are not supported by the entry.
        - Do not provide medical, psychological, or diagnostic conclusions.
        - Preserve uncertainty when the content is ambiguous.
        - Use the same language as the journal entry for the summary, mood, and tags.

        Summary:
        - Create a concise, factual summary.
        - The summary must contain no more than 30 characters.
        - Preserve the main meaning of the entry.
        - Do not add details that are not present in the content.

        Mood:
        - Return the predominant mood or emotion as one concise word.
        - Use the same language as the entry.
        - Choose the mood only when it is explicitly stated or
        strongly supported by the content.

        Sentiment score:
        - Return a number from -1.0 to 1.0.
        - Use -1.0 for strongly negative content.
        - Use 0.0 for neutral, unclear, balanced, or mixed content.
        - Use 1.0 for strongly positive content.
        - Use intermediate values proportionally.
        - Base the score on the overall emotional tone of the entry.

        Tags:
        - Generate no more than 5 tags.
        - Each tag must contain between 3 and 20 characters.
        - Tags must be unique, concise, relevant, and based only on the entry.
        - Prefer specific topics, emotions, events, activities, people, or contexts.
        - Reuse a matching tag from "Available existing tags" when it
          accurately represents the content.
        - Otherwise create a new tag in the same language as the entry.
        - Use nominative form where appropriate.
        - Do not translate existing tags.
        - Do not generate generic tags such as "journal", "entry", "life", or "thoughts"
        when a more specific tag is available.
        - Do not add tags for information that is not present in the entry.

        When the entry contains too little information, return a neutral and
        conservative analysis instead of guessing.
        """
        try:
            logger.debug("Fetching response from LLM")
            response = await self.client.responses.parse(
                model=self.model,
                instructions=system_prompt,
                input=user_prompt,
                text_format=EntryAnalysis,
                temperature=0.1,
                max_output_tokens=300,
            )
            logger.info("Returning a validated analysis data")
            return response.output_parsed
        except Exception:
            logger.exception("An error occured while analyzing entry data")
            return EntryAnalysis()

    async def get_embedding(self, content: str) -> list[float] | None:
        try:
            logger.debug("Fetching response from LLM")
            response = await self.client.embeddings.create(
                model=self.embedding_model,
                input=content,
            )
            logger.info("Returning generated embedding")
            return response.data[0].embedding
        except Exception:
            logger.exception("An error occured while generating an embedding")
