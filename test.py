
import pandas as pd
import sys

from src.utils.logger import get_logger
from src.utils.exception import CustomException

logger = get_logger(__name__)


def load_dataset(file_path):
    try:
        logger.info(f"Loading dataset: {file_path}")

        df = pd.read_csv(file_path)

        logger.info(
            f"Dataset loaded successfully. Shape: {df.shape}"
        )

        return df

    except Exception as error:
        logger.exception("Dataset loading failed.")
        raise CustomException(error, sys) from error
