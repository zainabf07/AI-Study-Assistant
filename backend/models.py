from pydantic import BaseModel, Field, field_validator


class TopicRequest(BaseModel):
    topic: str

    @field_validator("topic")
    @classmethod
    def topic_must_not_be_empty(cls, value: str) -> str:
        if not value or not value.strip():
            raise ValueError("Topic cannot be empty. Please enter a study topic.")
        return value.strip()


class StudyResponse(BaseModel):
    explanation: str = Field(description="A short explanation of the study topic")
    key_points: list[str] = Field(description="Exactly three important key points")
    quiz_questions: list[str] = Field(description="Exactly two quiz questions")
