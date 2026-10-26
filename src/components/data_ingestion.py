
import sys
import pandas as pd

from src.utils.logger import get_logger
from src.utils.exception import CustomException
from src.utils.config_loader import read_yaml, PROJECT_ROOT

logger = get_logger(__name__)


def load_dataset(dataset_type="train"):
    try:
        config = read_yaml("config.yaml")
        raw_data_dir = PROJECT_ROOT / config["paths"]["raw_data"]

        if dataset_type == "train":
            file_name = config["data"]["train_file"]
        elif dataset_type == "test":
            file_name = config["data"]["test_file"]
        else:
            raise ValueError(
                "dataset_type must be either 'train' or 'test'.")

        file_path = raw_data_dir / file_name

        logger.info(f"Loading {dataset_type} dataset from {file_path}")

        if not file_path.exists():
            raise FileNotFoundError(
                f"Dataset file not found: {file_path}")

        df = pd.read_csv(file_path)

        if df.empty:
            raise ValueError(
                f"The {dataset_type} dataset is empty: {file_path}"
            )

        logger.info(
            f"{dataset_type.capitalize()} dataset loaded successfully. "
            f"Shape: {df.shape}")

        return df

    except Exception as error:
        logger.exception(
            f"Failed to load the {dataset_type} dataset.")
        raise CustomException(error, sys) from error
