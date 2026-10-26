
from src.components.data_ingestion import load_dataset
from src.utils.logger import get_logger

logger = get_logger(__name__)


def main():
    train_df = load_dataset("train")
    test_df = load_dataset("test")

    print("\nData ingestion test results")
    print("-" * 30)
    print(f"Training shape: {train_df.shape}")
    print(f"Test shape: {test_df.shape}")
    print(f"Training columns: {train_df.columns.tolist()}")
    print(f"Test columns: {test_df.columns.tolist()}")

    print("\nFirst five training records:")
    print(train_df.head().to_string(index=False))

    logger.info("Data ingestion test completed successfully.")


if __name__ == "__main__":
    main()
