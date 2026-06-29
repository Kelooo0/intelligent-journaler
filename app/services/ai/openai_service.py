from datetime import UTC, datetime

from fastapi import HTTPException, status
from loguru import logger
from openai import AsyncOpenAI

from app.core.config import settings
from app.schemas.schemas import DatesSchema, EntryAnalysis, ResponseSchema, VectorResult
from app.services.ai.base import AIService


class OpenAIService(AIService):
    def __init__(self) -> None:
        logger.debug("Initializing OpenAI client")
        self.client = AsyncOpenAI()
        self.model = settings.OPENAI_MODEL
        self.embedding_model = settings.OPENAI_EMBEDDING_MODEL

    async def analyze_entry(self, content: str, tags: str) -> EntryAnalysis:
        logger.info("Analyzing entry content")
        logger.debug("Setting up prompts for analyzing entry content")
        user_prompt = f"""
            Content: {content}
            Available existing tags: {tags}
        """
        system_prompt = """
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
            response = await self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt},
                ],
                response_format=EntryAnalysis,
                temperature=0.1,
            )
            data = response.choices[0].message.parsed
            logger.info("Returning a validated analysis data")
            return data
        except Exception:
            logger.exception("An error occured while analyzing entry data")
            return EntryAnalysis()

    async def get_embedding(self, content: str) -> list[float] | None:
        try:
            logger.debug("Generating an embedding for provided content")
            response = await self.client.embeddings.create(
                model=self.embedding_model,
                input=content,
                dimensions=768,
            )
            logger.info("Returning generated embedding")
            return response.data[0].embedding
        except Exception:
            logger.exception("An error occured while generating an embedding")

    async def get_dates(self, query_content: str) -> DatesSchema:
        logger.debug("Fetching dates from provided query")
        current_date = datetime.now(UTC).strftime("%Y-%m-%d, %A")
        logger.debug("Setting up prompts for fetching dates")
        user_prompt = f"""
        Today is {current_date}.
        User: {query_content}
        """
        system_prompt = (
            "Extract date ranges from the user's query according to the schema."
        )
        try:
            logger.debug("Fetching response from LLM model")
            response = await self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {"role": "user", "content": user_prompt},
                ],
                response_format=DatesSchema,
                temperature=0.0,
            )
            data = response.choices[0].message.parsed
            logger.debug(
                "Dates returned from AI: SD: {}, ED: {}",
                data.start_date or "None",
                data.end_date or "None",
            )
            logger.info("Returning validated dates")
            return data
        except Exception:
            logger.exception("An error occured while fetching dates")
            return DatesSchema()

    async def transform_query(self, query_content: str) -> str:
        logger.debug("Transforming user query into a LLM-friendly form")
        logger.debug("Setting up prompt for transforming user query")
        system_prompt = """
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
        """
        try:
            logger.debug("Fetching response from LLM model")
            response = await self.client.responses.create(
                model=self.model,
                input=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {"role": "user", "content": query_content},
                ],
                temperature=0.0,
                max_output_tokens=60,
            )
            text = response.output_text
            logger.debug(f"Transformed user query: {text}")
            logger.info("Returning transformed user query")
            return text
        except Exception:
            logger.exception("An error occured while transforming user query")
            return query_content

    async def assistant_response(
        self, query_content: str, vector_result: list[VectorResult]
    ) -> ResponseSchema:
        logger.debug("Generating proper AI response")
        clean_query = await self.transform_query(query_content)
        logger.debug("Preparing context from matching entries")
        context = ""
        for i, result in enumerate(vector_result):
            context += f"ENTRY {i + 1}:\n"
            context += f"- Entry ID: {result.entry.id}\n"
            context += f"- Content: {result.entry.content}\n"
            context += f"- Mood: {result.entry.mood}\n"
            context += f"- Created at: {result.entry.created_at}\n"
            context += f"- Relevance score: {result.relevance_score}\n"
        logger.debug("Setting up prompts for assistant response")
        user_prompt = f"""
        <journal_context>
        "{context}"
        </journal_context>

        USER QUERY:
        "{clean_query}"
        """
        system_prompt = """
        You are an advanced, empathetic, and secure AI Diary Assistant.
        Your purpose is to help the user analyze their personal journal entries,
        discover emotional patterns, and recall past events.

        <CONTEXT_RULES>
        - You are provided with relevant journal entries matching the user's request
        inside the <journal_context> tag.
        - Base your response ONLY and EXCLUSIVELY on the provided journal entries.
        - Never hallucinate or use external world knowledge about the user.
        When filling the `used_entries` list:
            - Copy the `id` and `relevance_score` values exactly from the corresponding journal entries.
            - Do not generate, modify, or infer these values.
        </CONTEXT_RULES>

        <STYLE_AND_TONE>
        - Language Match (CRITICAL): Always respond in the exact same language that the user used in their query
        (e.g., if the user asks in Polish, respond in Polish; if in English, respond in English).
        - Perspective: Speak directly to the user in the 2nd person singular (e.g., "You wrote...", "Your notes indicate that...", "You felt...").
        - Tone: Warm, supportive, empathetic, and objective. Act like a trusted, non-judgmental companion or a personal coach.
        - Precision: Be concise and factual. Reference specific dates or timeframes provided in the context
        (e.g., "On March 15, you mentioned that..."). Do not over-analyze or preach.
        </STYLE_AND_TONE>
        """
        try:
            logger.debug("Fetching response from LLM model")
            response = await self.client.beta.chat.completions.parse(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": system_prompt,
                    },
                    {"role": "user", "content": user_prompt},
                ],
                temperature=0.2,
                max_completion_tokens=800,
                top_p=0.95,
                response_format=ResponseSchema,
            )
            data = response.choices[0].message.parsed
            logger.info("Returning response from AI assistant")
            return data
        except Exception as e:
            logger.exception("An error occured while generating AI response")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="An error occured while generating AI response",
            ) from e
