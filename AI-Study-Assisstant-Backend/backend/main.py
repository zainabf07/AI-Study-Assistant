import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types

from .models import StudyResponse, TopicRequest

ENV_FILE = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(ENV_FILE, override=True)

app = FastAPI(title="AI Study Assistant")

GEMINI_MODEL = "gemini-3.5-flash"

GEMINI_FAILURE_MESSAGE = (
    "The AI service is unavailable right now. Please try again in a moment."
)
UNEXPECTED_AI_MESSAGE = (
    "The AI returned an unexpected response. Please try again."
)


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


def is_complete_study_material(material: StudyResponse) -> bool:
    if not material.explanation or not material.explanation.strip():
        return False
    if len(material.key_points) != 3 or len(material.quiz_questions) != 2:
        return False
    if any(not point or not str(point).strip() for point in material.key_points):
        return False
    if any(
        not question or not str(question).strip()
        for question in material.quiz_questions
    ):
        return False
    return True


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
        raise HTTPException(status_code=502, detail=GEMINI_FAILURE_MESSAGE)

    try:
        study_material = _parse_study_response(response)
    except HTTPException:
        raise
    except Exception:
        raise HTTPException(status_code=502, detail=UNEXPECTED_AI_MESSAGE)

    if not is_complete_study_material(study_material):
        raise HTTPException(status_code=502, detail=UNEXPECTED_AI_MESSAGE)

    return study_material


def _parse_study_response(response: object) -> StudyResponse:
    parsed = getattr(response, "parsed", None)
    if isinstance(parsed, StudyResponse):
        return parsed
    if isinstance(parsed, dict):
        try:
            return StudyResponse.model_validate(parsed)
        except Exception:
            pass

    text = getattr(response, "text", None)
    if text:
        try:
            return StudyResponse.model_validate_json(text)
        except Exception:
            pass

    raise HTTPException(status_code=502, detail=UNEXPECTED_AI_MESSAGE)
