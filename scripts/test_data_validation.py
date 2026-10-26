
from src.components.data_ingestion import load_dataset
from src.components.data_validation import validate_dataset


def main():
    train_df = load_dataset("train")
    test_df = load_dataset("test")

    validate_dataset(train_df, "train")
    validate_dataset(test_df, "test")

    print("Training dataset validation: PASSED")
    print("Test dataset validation: PASSED")


if __name__ == "__main__":
    main()
