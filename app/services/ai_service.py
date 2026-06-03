import json

from fastapi import HTTPException, status
from google import genai
from google.genai import types

from app.config import settings
from app.schemas import EntryAnalysis


class AIService:
    def __init__(self) -> None:
        self.client = genai.Client(api_key=settings.API_KEY)
        self.model_id = "gemini-2.5-flash"

    async def analyze_entry(self, content: str, tags: str) -> EntryAnalysis:
        try:
            prompt = f"""
                Content: {content}
                Available existing tags: {tags}

                TASK:
                Analyze the journal entry provided in 'Content'.

                LANGUAGE:
                Respond in the same language as the Content.

                RULES FOR TAGS:
                1. Every tag must be a noun in the singular form (base form, e.g., "training", "work", "sadness").
                2. Never use plurals, verbs, or inflected forms (e.g., DO NOT use "trainings", "working", "sadly").
                3. Write all tags in lowercase.
            """
            response = await self.client.aio.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json",
                    response_schema=EntryAnalysis,
                    temperature=0.1,
                ),
            )
            data = EntryAnalysis.model_validate_json(response.text)
            return data
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="An AIService error occured",
            )


ai_service = AIService()
