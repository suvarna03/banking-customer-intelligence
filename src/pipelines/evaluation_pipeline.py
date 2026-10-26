import json
from pathlib import Path

import joblib
import pandas as pd

from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,
)

from src.utils.config_loader import read_yaml
from src.utils.logger import get_logger
from src.utils.exception import CustomException


logger = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def run_evaluation_pipeline():
    try:
        logger.info("Starting final test evaluation")

        config = read_yaml("config.yaml")
        schema = read_yaml("schema.yaml")

        test_path = (
            PROJECT_ROOT
            / config["paths"]["raw_data"]
            / config["data"]["test_file"])

        model_path = (
            PROJECT_ROOT
            / config["paths"]["models"]
            / "best_banking77_pipeline.joblib")

        artifacts_path = (
            PROJECT_ROOT
            / config["paths"]["artifacts"]
            / "phase_4")
        artifacts_path.mkdir(parents=True, exist_ok=True)

        if not test_path.exists():
            raise FileNotFoundError(
                f"Test dataset not found: {test_path}")

        if not model_path.exists():
            raise FileNotFoundError(
                f"Trained pipeline not found: {model_path}")

        df = pd.read_csv(test_path)

        text_column = schema["dataset"]["text_column"]
        target_column = schema["dataset"]["target_column"]

        if df.empty:
            raise ValueError("Test dataset is empty")

        if df[[text_column, target_column]].isnull().any().any():
            raise ValueError("Missing values found in test dataset")

        X_test = df[text_column].astype(str)
        y_test = df[target_column].astype(str)

        model = joblib.load(model_path)

        y_pred = model.predict(X_test)

        accuracy = accuracy_score(y_test, y_pred)
        macro_f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)
        weighted_f1 = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        report = classification_report(
            y_test,
            y_pred,
            output_dict=True,
            zero_division=0)

        results = {
            "test_samples": int(len(df)),
            "accuracy": float(accuracy),
            "macro_f1": float(macro_f1),
            "weighted_f1": float(weighted_f1),
            "model": "LinearSVC with TF-IDF",}

        with open(
            artifacts_path / "test_evaluation_results.json","w",
            encoding="utf-8") as file:
                json.dump(results, file, indent=4)

        with open(
            artifacts_path / "test_classification_report.json","w",
            encoding="utf-8") as file:
                json.dump(report, file, indent=4)

        logger.info("Final test evaluation completed")
        logger.info("Test accuracy: %.4f", accuracy)
        logger.info("Test macro F1: %.4f", macro_f1)
        logger.info("Test weighted F1: %.4f", weighted_f1)

        print("\nFINAL TEST RESULTS")
        print("-" * 40)
        print(f"Test samples: {len(df)}")
        print(f"Accuracy: {accuracy:.4f}")
        print(f"Macro F1: {macro_f1:.4f}")
        print(f"Weighted F1: {weighted_f1:.4f}")

        print(
            "\nResults saved to:",
            artifacts_path / "test_evaluation_results.json" )

        return results

    except Exception as e:
        logger.exception("Final test evaluation failed")
        raise CustomException(e) from e


if __name__ == "__main__":
    run_evaluation_pipeline()
