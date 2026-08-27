import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types

from models import StudyResponse, TopicRequest

load_dotenv()
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

app = FastAPI(title="AI Study Assistant")

GEMINI_MODEL = "gemini-2.0-flash"


def get_gemini_client() -> genai.Client:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key or api_key.strip() in {"", "your_gemini_api_key_here"}:
        raise HTTPException(
            status_code=500,
            detail="The study assistant is not configured. Set GEMINI_API_KEY in the .env file.",
        )
    return genai.Client(api_key=api_key.strip())


def build_prompt(topic: str) -> str:
    return (
        "You are a study assistant for students. "
        f'Create study material for this topic: "{topic}". '
        "Return a short explanation, exactly three important key points, "
        "and exactly two quiz questions about the topic."
    )


@app.get("/")
def read_root() -> dict[str, str]:
    return {"status": "ok", "message": "AI Study Assistant API is running"}


@app.post("/generate", response_model=StudyResponse)
def generate_study_material(request: TopicRequest) -> StudyResponse:
    try:
        client = get_gemini_client()
        response = client.models.generate_content(
            model=GEMINI_MODEL,
            contents=build_prompt(request.topic),
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=StudyResponse,
            ),
        )
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(
            status_code=502,
            detail="Unable to generate study material. The AI service failed. Please try again.",
        )

    study_material = _parse_study_response(response)

    if len(study_material.key_points) != 3 or len(study_material.quiz_questions) != 2:
        raise HTTPException(
            status_code=502,
            detail="Unable to generate study material. The AI service returned an incomplete response. Please try again.",
        )

    return study_material


def _parse_study_response(response: object) -> StudyResponse:
    parsed = getattr(response, "parsed", None)
    if isinstance(parsed, StudyResponse):
        return parsed

    text = getattr(response, "text", None)
    if text:
        try:
            return StudyResponse.model_validate_json(text)
        except Exception:
            pass

    raise HTTPException(
        status_code=502,
        detail="Unable to generate study material. The AI service returned an invalid response. Please try again.",
    )
