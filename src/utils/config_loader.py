
from pathlib import Path

import yaml

from src.utils.logger import get_logger
from src.utils.exception import CustomException
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"

logger = get_logger(__name__)


def read_yaml(file_name):
    file_path = CONFIG_DIR / file_name

    try:
        if not file_path.exists():
            raise FileNotFoundError(
                f"Configuration file not found: {file_path}"
            )

        with open(file_path, "r", encoding="utf-8") as file:
            config = yaml.safe_load(file)

        if config is None:
            raise ValueError(
                f"Configuration file is empty: {file_path}"
            )

        logger.info(f"Configuration loaded: {file_name}")

        return config

    except Exception as error:
        logger.exception(
            f"Failed to read configuration: {file_name}"
        )
        raise CustomException(error, sys) from error
