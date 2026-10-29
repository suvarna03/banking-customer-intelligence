
import joblib

from src.utils.config_loader import PROJECT_ROOT
from src.utils.logger import get_logger

logger = get_logger(__name__)

MODEL_PATH = PROJECT_ROOT / "models" / "best_banking77_pipeline.joblib"

model = None


def load_model():
    global model

    if model is None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                f"Trained model not found: {MODEL_PATH}"
            )

        model = joblib.load(MODEL_PATH)
        logger.info("Banking intent model loaded.")

    return model


def predict_intent(text):
    if not isinstance(text, str) or not text.strip():
        raise ValueError("Customer message cannot be empty.")

    trained_model = load_model()
    prediction = trained_model.predict([text.strip()])[0]

    return {
        "text": text.strip(),
        "intent": str(prediction)
    }
