from fastapi import HTTPException, status
from google import genai
from google.genai import types
from loguru import logger

from app.models.models import EntryModel
from app.schemas.schemas import EntryAnalysis


class AIService:
    def __init__(self) -> None:
        logger.debug("Initializing genai client")
        self.client = genai.Client().aio
        self.model_id = "gemini-2.5-flash"
        self.embedding_model = "gemini-embedding-001"

    async def analyze_entry(self, content: str, tags: str) -> EntryAnalysis:
        logger.info("Analyzing entry content")
        logger.debug("Preparing prompt")
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
        try:
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

    async def assistant_response(
        self, user_query: str, matching_entries: list[EntryModel]
    ) -> dict[str, str]:
        logger.info("Generating proper AI response")
        logger.debug("Formatting entries")
        formatted_entries = [
            {"content": e.content, "created_at": e.created_at.strftime("%Y-%m-%d")}
            for e in matching_entries
        ]
        logger.debug("Preparing string context from formatted entries")
        context = ""
        for i, entry in enumerate(formatted_entries):
            context += f"ENTRY {i + 1}:\n"
            context += f"- Content: {entry['content']}\n"
            context += f"- Created at: {entry['created_at']}\n"
        logger.debug("Preparing prompt")
        prompt = f"""
        You are an advanced, empathetic, and secure AI Diary Assistant.
        Your purpose is to help the user analyze their personal journal entries,
        discover emotional patterns, and recall past events.

        <CONTEXT_RULES>
        - You are provided with relevant journal entries matching the user's request
        inside the <journal_context> tag.
        - Base your response ONLY and EXCLUSIVELY on the provided journal entries.
        - If the provided entries do not contain enough information to answer the question,
        or if the context is empty, respond exactly with: "I could not find information in your journal that
        would allow me to answer this question." (or the equivalent in the user's language).
        - Never hallucinate or use external world knowledge about the user.
        </CONTEXT_RULES>

        <STYLE_AND_TONE>
        - Language Match (CRITICAL): Always respond in the exact same language that the user used in their query
        (e.g., if the user asks in Polish, respond in Polish; if in English, respond in English).
        - Perspective: Speak directly to the user in the 2nd person singular (e.g., "You wrote...", "Your notes indicate that...", "You felt...").
        - Tone: Warm, supportive, empathetic, and objective. Act like a trusted, non-judgmental companion or a personal coach.
        - Precision: Be concise and factual. Reference specific dates or timeframes provided in the context
        (e.g., "On March 15, you mentioned that..."). Do not over-analyze or preach.
        </STYLE_AND_TONE>

        <journal_context>
        "{context}"
        </journal_context>

        USER QUERY:
        "{user_query}"
        """
        try:
            response = await self.client.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=800,
                    top_p=0.95,
                    top_k=40,
                ),
            )
            return {"answer": response.text}
        except Exception as e:
            logger.exception("An error occured while generating AI response")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="An error occured while generating AI response",
            ) from e


ai_service = AIService()
