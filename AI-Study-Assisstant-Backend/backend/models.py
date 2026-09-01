from pydantic import BaseModel, Field, field_validator

MAX_TOPIC_LENGTH = 300


class TopicRequest(BaseModel):
    topic: str

    @field_validator("topic")
    @classmethod
    def topic_must_be_valid(cls, value: str) -> str:
        if not value or not str(value).strip():
            raise ValueError("Topic cannot be empty. Please enter a study topic.")
        topic = str(value).strip()
        if len(topic) > MAX_TOPIC_LENGTH:
            raise ValueError(
                "That topic is too long. Please enter a shorter study topic."
            )
        return topic


class StudyResponse(BaseModel):
    explanation: str = Field(description="A short explanation of the study topic")
    key_points: list[str] = Field(description="Exactly three important key points")
    quiz_questions: list[str] = Field(description="Exactly two quiz questions")
