from fastapi.testclient import TestClient

from src.api.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_intent():
    response = client.post(
        "/predict-intent",
        json={"text": "I want to check my bank balance"}
    )

    assert response.status_code == 200
    assert response.json()["text"] == "I want to check my bank balance"
    assert isinstance(response.json()["intent"], str)


def test_ask_banking_question():
    response = client.post(
        "/ask",
        json={"question": "What should I do if my payment card is lost?"}
    )

    assert response.status_code == 200

    result = response.json()

    assert result["status"] == "answered"
    assert result["answer"]
    assert len(result["sources"]) > 0


def test_empty_intent_message():
    response = client.post(
        "/predict-intent",
        json={"text": ""}
    )

    assert response.status_code == 422