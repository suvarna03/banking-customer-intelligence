
from fastapi import FastAPI, HTTPException

from src.api.schemas import (
    IntentRequest,
    IntentResponse,
    QuestionRequest,
    AnswerResponse,
)
from src.components.intent_prediction import predict_intent
from src.components.answer_graph import ask_banking_question
from src.utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(
    title="Banking Customer Intelligence API",
    description=(
        "API for banking intent classification and "
        "evidence-based customer question answering."
    ),
    version="1.0.0",
)


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "Banking Customer Intelligence API",
    }


@app.post("/predict-intent", response_model=IntentResponse)
def predict_customer_intent(request: IntentRequest):
    try:
        result = predict_intent(request.text)
        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        logger.exception("Intent prediction failed.")

        raise HTTPException(
            status_code=500,
            detail="Intent prediction failed.",
        ) from error


@app.post("/ask", response_model=AnswerResponse)
def answer_banking_question(request: QuestionRequest):
    try:
        result = ask_banking_question(request.question)
        return result

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        ) from error

    except Exception as error:
        logger.exception("Banking question answering failed.")

        raise HTTPException(
            status_code=500,
            detail="Unable to process the banking question.",
        ) from error
