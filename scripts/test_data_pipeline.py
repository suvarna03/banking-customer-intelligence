
from src.pipelines.data_pipeline import run_data_pipeline


def main():
    train_df = run_data_pipeline("train")
    test_df = run_data_pipeline("test")

    print("\nData pipeline test results")
    print("-" * 30)
    print(f"Training data shape: {train_df.shape}")
    print(f"Test data shape: {test_df.shape}")
    print("Training pipeline: PASSED")
    print("Test pipeline: PASSED")


if __name__ == "__main__":
    main()
