from datetime import UTC, datetime

from fastapi import HTTPException, status
from google import genai
from google.genai import types
from loguru import logger

from app.models.models import EntryModel
from app.schemas.schemas import DatesSchema, EntryAnalysis


class AIService:
    def __init__(self) -> None:
        logger.debug("Initializing genai client")
        self.client = genai.Client().aio
        self.model = "gemini-2.5-flash"
        self.model_lite = "gemini-2.5-flash-lite"
        self.embedding_model = "gemini-embedding-001"

    async def analyze_entry(self, content: str, tags: str) -> EntryAnalysis:
        logger.info("Analyzing entry content")
        logger.debug("Setting up prompt for analyzing entry content")
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
            logger.debug("Fetching response from LLM model")
            response = await self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=EntryAnalysis,
                    temperature=0.1,
                ),
            )
            data = EntryAnalysis.model_validate_json(response.text)
            logger.info("Returning a validated analysis data")
            return data
        except Exception:
            logger.exception("An error occured while analyzing entry data")
            return EntryAnalysis()

    async def get_embedding(self, content: str) -> list[float] | None:
        try:
            logger.debug("Generating an embedding for provided content")
            response = await self.client.models.embed_content(
                model=self.embedding_model,
                contents=content,
                config=types.EmbedContentConfig(output_dimensionality=768),
            )
            logger.info("Returning generated embedding")
            return response.embeddings[0].values
        except Exception:
            logger.exception("An error occured while generating an embedding")

    async def get_dates(self, query_content: str) -> DatesSchema:
        logger.debug("Fetching dates from provided query")
        current_date = datetime.now(UTC).strftime("%Y-%m-%d, %A")
        logger.debug("Setting up prompt for fetching dates")
        prompt = f"""
        Today is {current_date}.
        Extract date ranges from the user's query according to the schema.
        User: {query_content}
        """
        try:
            logger.debug("Fetching response from LLM model")
            response = await self.client.models.generate_content(
                model=self.model_lite,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=DatesSchema,
                    temperature=0.0,
                ),
            )
            data = DatesSchema.model_validate_json(response.text)
            logger.info("Returning validated dates")
            return data
        except Exception:
            logger.exception("An error occured while fetching dates")
            return DatesSchema()

    async def transform_query(self, query_content: str) -> str:
        logger.debug("Transforming user query into a LLM-friendly form")
        logger.debug("Setting up prompt for transforming user query")
        prompt = f"""
        You are a query optimization module in a smart journal application.
        Your task is to transform a chaotic, colloquial user question into a dense keyword
        phrase optimized for semantic (vector) search in the database.

        RULES:
        1. Remove personal and demonstrative pronouns (e.g., 'I', 'he', 'she', 'then', 'there', 'it', 'this').
        2. Extract key emotions, events, people, or topics that the query is about.
        3. If the user asks about a specific time (e.g., "yesterday", "a year ago"),
        ignore the time aspect (time filtering is handled by another module) and focus solely on the core topic.
        4. Output ONLY the generated search phrase in user's language.
        Do not add any introductory text, quotes, or explanations.

        EXAMPLES:
        User: "Why did I get so incredibly mad at him back then?"
        Phrase: "argument anger at boyfriend reasons for irritation negative emotions"

        User: "Where did I hide those car documents I wrote about last month?"
        Phrase: "lost car documents hiding place papers auto vehicle"

        User: "How did I feel when my dog passed away?"
        Phrase: "dog death sadness grief loss of pet emotions"

        User: "{query_content}"
        """
        try:
            logger.debug("Fetching response from LLM model")
            response = await self.client.models.generate_content(
                model=self.model_lite,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.0, max_output_tokens=60
                ),
            )
            logger.info("Returning transformed user query")
            return response.text
        except Exception:
            logger.exception("An error occured while transforming user query")
            return query_content

    async def assistant_response(
        self, query_content: str, matching_entries: list[EntryModel]
    ) -> dict[str, str]:
        logger.debug("Generating proper AI response")
        clean_query = await self.transform_query(query_content)
        logger.debug("Formatting matching entries")
        formatted_entries = [
            {"content": e.content, "created_at": e.created_at.strftime("%Y-%m-%d")}
            for e in matching_entries
        ]
        logger.debug("Preparing context from formatted entries")
        context = ""
        for i, entry in enumerate(formatted_entries):
            context += f"ENTRY {i + 1}:\n"
            context += f"- Content: {entry['content']}\n"
            context += f"- Created at: {entry['created_at']}\n"
        logger.debug("Setting up prompt for assistant response")
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
        "{clean_query}"
        """
        try:
            logger.debug("Fetching response from LLM model")
            response = await self.client.models.generate_content(
                model=self.model,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0.2,
                    max_output_tokens=800,
                    top_p=0.95,
                    top_k=40,
                ),
            )
            logger.info("Returning response from AI assistant")
            return {"answer": response.text}
        except Exception as e:
            logger.exception("An error occured while generating AI response")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="An error occured while generating AI response",
            ) from e


ai_service = AIService()
