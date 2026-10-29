
from pydantic import BaseModel, Field


class IntentRequest(BaseModel):
    text: str = Field(
        min_length=1,
        max_length=5000,
        description="Customer banking message"
    )


class IntentResponse(BaseModel):
    text: str
    intent: str


class QuestionRequest(BaseModel):
    question: str = Field(
        min_length=1,
        max_length=5000,
        description="Customer banking question"
    )


class SourceResponse(BaseModel):
    title: str
    publisher: str
    url: str
    similarity: float


class AnswerResponse(BaseModel):
    question: str
    answer: str
    sources: list[SourceResponse]
    status: str
