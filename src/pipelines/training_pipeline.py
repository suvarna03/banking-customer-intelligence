
import json
import sys
from pathlib import Path

import joblib
import pandas as pd
from scipy.sparse import load_npz
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    classification_report,)
from sklearn.svm import LinearSVC

from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.utils.config_loader import PROJECT_ROOT

logger = get_logger(__name__)

ARTIFACT_DIR = PROJECT_ROOT / "artifacts" / "phase_4"
MODEL_DIR = PROJECT_ROOT / "models"


def load_labels(file_path):
    labels_df = pd.read_csv(file_path)

    if labels_df.empty:
        raise ValueError(f"No labels found in {file_path}")

    return labels_df.iloc[:, -1]


def run_training_pipeline():
    try:
        logger.info("Starting model training pipeline.")

        X_train = load_npz(ARTIFACT_DIR / "X_train_tfidf.npz")
        X_val = load_npz(ARTIFACT_DIR / "X_val_tfidf.npz")

        y_train = load_labels(ARTIFACT_DIR / "y_train.csv")
        y_val = load_labels(ARTIFACT_DIR / "y_val.csv")

        if X_train.shape[0] != len(y_train):
            raise ValueError("Training features and labels have different lengths.")

        if X_val.shape[0] != len(y_val):
            raise ValueError("Validation features and labels have different lengths.")

        logger.info(f"Training feature shape: {X_train.shape}")
        logger.info(f"Validation feature shape: {X_val.shape}")

        models = {
            "logistic_regression": LogisticRegression(
                max_iter=1000,
                random_state=42),
            "linear_svm": LinearSVC(
                random_state=42,
                max_iter=3000)
            }

        results = {}
        best_model = None
        best_model_name = None
        best_macro_f1 = -1.0

        for model_name, model in models.items():
            logger.info(f"Training {model_name}.")

            model.fit(X_train, y_train)
            predictions = model.predict(X_val)

            accuracy = accuracy_score(y_val, predictions)
            macro_f1 = f1_score(y_val, predictions, average="macro", zero_division=0)
            weighted_f1 = f1_score(y_val, predictions, average="weighted", zero_division=0)

            results[model_name] = {
                "accuracy": float(accuracy),
                "macro_f1": float(macro_f1),
                "weighted_f1": float(weighted_f1)}

            logger.info(
                f"{model_name}: accuracy={accuracy:.4f}, "
                f"macro_f1={macro_f1:.4f}, "
                f"weighted_f1={weighted_f1:.4f}")

            if macro_f1 > best_macro_f1:
                best_macro_f1 = macro_f1
                best_model = model
                best_model_name = model_name

        MODEL_DIR.mkdir(parents=True, exist_ok=True)

        model_path = MODEL_DIR / "best_tfidf_model.joblib"
        joblib.dump(best_model, model_path)

        best_predictions = best_model.predict(X_val)

        report = classification_report(
            y_val,
            best_predictions,
            output_dict=True,
            zero_division=0)

        report_path = ARTIFACT_DIR / "validation_classification_report.json"
        with open(report_path, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

        results_path = ARTIFACT_DIR / "training_results.json"
        with open(results_path, "w", encoding="utf-8") as file:
            json.dump(results, file, indent=4)

        logger.info(f"Best model: {best_model_name}")
        logger.info(f"Saved model to {model_path}")
        logger.info(f"Saved validation report to {report_path}")

        print("\nValidation Results")
        print("-" * 45)

        for name, metrics in results.items():
            print(
                f"{name}: "
                f"Accuracy={metrics['accuracy']:.4f}, "
                f"Macro F1={metrics['macro_f1']:.4f}, "
                f"Weighted F1={metrics['weighted_f1']:.4f}"
            )

        print(f"\nSelected model: {best_model_name}")
        print(f"Saved model: {model_path}")

        return best_model, results

    except Exception as error:
        logger.exception("Model training pipeline failed.")
        raise CustomException(error, sys) from error
