
import sys

from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.utils.config_loader import read_yaml

logger = get_logger(__name__)


def validate_dataset(df, dataset_type="train"):
    try:
        schema = read_yaml("schema.yaml")
        required_columns = schema["dataset"]["required_columns"]
        target_column = schema["dataset"]["target_column"]
        text_column = schema["dataset"]["text_column"]
        expected_classes = schema["dataset"]["expected_intent_classes"]

        logger.info(f"Validating {dataset_type} dataset.")

        if df.empty:
            raise ValueError(f"The {dataset_type} dataset is empty.")

        missing_columns = set(required_columns) - set(df.columns)

        if missing_columns:
            raise ValueError(
                f"Missing required columns: {sorted(missing_columns)}")

        missing_values = df[required_columns].isnull().sum()

        if missing_values.any():
            missing_details = missing_values[missing_values > 0].to_dict()
            raise ValueError(
                f"Missing values found in {dataset_type} dataset: "
                f"{missing_details}")

        empty_text_count = (
            df[text_column].astype(str).str.strip().eq("").sum())

        if empty_text_count > 0:
            raise ValueError(
                f"Found {empty_text_count} empty text values.")

        if df[target_column].astype(str).str.strip().eq("").any():
            raise ValueError("Empty intent labels were found.")

        if dataset_type == "train":
            class_count = df[target_column].nunique()

            if class_count != expected_classes:
                raise ValueError(
                    f"Expected {expected_classes} intent classes, "
                    f"but found {class_count}.")

        logger.info(
            f"{dataset_type.capitalize()} dataset validation passed. "
            f"Shape: {df.shape}")

        return True

    except Exception as error:
        logger.exception(
            f"Validation failed for the {dataset_type} dataset.")
        raise CustomException(error, sys) from error
