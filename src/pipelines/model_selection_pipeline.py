import json
import time
from pathlib import Path

import pandas as pd
import joblib

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import GridSearchCV, StratifiedKFold
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.metrics import f1_score

from src.utils.config_loader import read_yaml
from src.utils.logger import get_logger
from src.utils.exception import CustomException


logger = get_logger(__name__)

PROJECT_ROOT = Path(__file__).resolve().parents[2]


def run_model_selection_pipeline():
    try:
        logger.info("Starting model selection pipeline")

        config = read_yaml("config.yaml")
        schema = read_yaml("schema.yaml")

        raw_data_path = (
            PROJECT_ROOT
            / config["paths"]["raw_data"]
            / config["data"]["train_file"] )

        artifacts_path = PROJECT_ROOT / config["paths"]["artifacts"] / "phase_4"
        models_path = PROJECT_ROOT / config["paths"]["models"]

        artifacts_path.mkdir(parents=True, exist_ok=True)
        models_path.mkdir(parents=True, exist_ok=True)

        df = pd.read_csv(raw_data_path)

        text_column = schema["dataset"]["text_column"]
        target_column = schema["dataset"]["target_column"]

        if df.empty:
            raise ValueError("Training dataset is empty")

        if text_column not in df.columns or target_column not in df.columns:
            raise ValueError("Required text or target column is missing")

        if df[[text_column, target_column]].isnull().any().any():
            raise ValueError("Missing values found in text or target columns")

        X = df[text_column].astype(str)
        y = df[target_column].astype(str)

        logger.info("Training dataset shape: %s", df.shape)
        logger.info("Number of intent classes: %s", y.nunique())

        expected_classes = schema["dataset"]["expected_intent_classes"]

        if y.nunique() != expected_classes:
            raise ValueError(
                f"Expected {expected_classes} intent classes, "
                f"but found {y.nunique()}")

        pipeline = Pipeline([
            (
                "tfidf",
                TfidfVectorizer(
                    strip_accents="unicode",
                    sublinear_tf=True
                )
            ),
            (
                "classifier",
                LinearSVC(
                    random_state=42,
                    max_iter=5000
                )
            )
        ])

        parameter_grid = {
            "tfidf__ngram_range": [(1, 1), (1, 2)],
            "tfidf__min_df": [1, 2],
            "tfidf__max_features": [20000],
            "classifier__C": [0.5, 1, 2, 5]
        }

        cv = StratifiedKFold(
            n_splits=5,
            shuffle=True,
            random_state=42
        )

        search = GridSearchCV(
            estimator=pipeline,
            param_grid=parameter_grid,
            scoring="f1_macro",
            cv=cv,
            n_jobs=1,
            verbose=2,
            refit=True,
            return_train_score=False,
            error_score="raise"
        )

        start_time = time.time()

        logger.info("Starting 5-fold cross-validation")
        search.fit(X, y)

        elapsed_time = round(time.time() - start_time, 2)

        best_pipeline = search.best_estimator_
        best_index = search.best_index_

        best_cv_macro_f1 = float(search.best_score_)
        best_cv_std = float(
            search.cv_results_["std_test_score"][best_index]
        )

        best_params = {
            key: (
                list(value)
                if isinstance(value, tuple)
                else value
            )
            for key, value in search.best_params_.items()}

        cv_results = pd.DataFrame(search.cv_results_)
        cv_results = cv_results.sort_values( by="rank_test_score")

        cv_results.to_csv(
            artifacts_path / "cross_validation_results.csv",
            index=False )

        model_path = models_path / "best_banking77_pipeline.joblib"
        joblib.dump(best_pipeline, model_path)

        results = {
            "selection_metric": "f1_macro",
            "cross_validation_folds": 5,
            "number_of_configurations": len(parameter_grid["tfidf__ngram_range"])
            * len(parameter_grid["tfidf__min_df"])
            * len(parameter_grid["tfidf__max_features"])
            * len(parameter_grid["classifier__C"]),
            "best_cv_macro_f1": best_cv_macro_f1,
            "best_cv_std": best_cv_std,
            "best_params": best_params,
            "elapsed_seconds": elapsed_time,
            "training_samples": int(len(df)),
            "intent_classes": int(y.nunique()),
            "model_path": str(model_path.relative_to(PROJECT_ROOT))
        }

        with open(
            artifacts_path / "model_selection_results.json","w",
            encoding="utf-8") as file:
            json.dump(results, file, indent=4)

        logger.info("Best CV macro F1: %.4f", best_cv_macro_f1)
        logger.info("CV macro F1 standard deviation: %.4f", best_cv_std)
        logger.info("Best parameters: %s", best_params)
        logger.info("Model saved to: %s", model_path)
        logger.info("Model selection completed in %s seconds", elapsed_time)

        print("\nMODEL SELECTION RESULTS")
        print("-" * 40)
        print(f"Best CV macro F1: {best_cv_macro_f1:.4f}")
        print(f"CV macro F1 standard deviation: {best_cv_std:.4f}")
        print(f"Best parameters: {best_params}")
        print(f"Elapsed time: {elapsed_time} seconds")
        print(f"Saved model: {model_path}")

        return results

    except Exception as e:
        logger.exception("Model selection pipeline failed")
        raise CustomException(e) from e


if __name__ == "__main__":
    run_model_selection_pipeline()
