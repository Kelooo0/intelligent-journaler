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
                Analyze the journal entry provided in "Content".
                1. Summary: Create a very short summary (max 30 chars).
                2. Mood: Identify the predominant emotion in one word.
                3. Sentiment: Score it from -1.0 (negative) to 1.0 (positive).
                4. Tags: Generate up to 5 relevant tags. Use matching tags from "Available existing tags" if they fit; otherwise, create new ones in the same language as the content (nominative case).

                LANGUAGE:
                Respond in the same language as the Content.

                FORMAT:
                Return ONLY a JSON object. No preamble, no markdown code blocks.
                {{
                    "summary": "...",
                    "mood": "...",
                    "sentiment_score": 0.0,
                    "tags": ["tag1", "tag2"]
                }}
            """
            response = await self.client.aio.models.generate_content(
                model=self.model_id,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                ),
            )
            print(response.text)
            data = json.loads(response.text)
            return EntryAnalysis(**data)
        except Exception as exc:
            raise HTTPException(status_code=status.HTTP_502_BAD_GATEWAY, detail=f"An AIService error occured, {exc}")


ai_service = AIService()
