
import sys

from src.components.data_ingestion import load_dataset
from src.components.data_validation import validate_dataset
from src.utils.logger import get_logger
from src.utils.exception import CustomException

logger = get_logger(__name__)


def run_data_pipeline(dataset_type="train"):
    try:
        logger.info(f"Starting data pipeline for {dataset_type} dataset.")

        df = load_dataset(dataset_type)
        validate_dataset(df, dataset_type)

        logger.info(
            f"Data pipeline completed successfully for {dataset_type}.")
        return df

    except Exception as error:
        logger.exception(
            f"Data pipeline failed for {dataset_type} dataset.")
        raise CustomException(error, sys) from error
