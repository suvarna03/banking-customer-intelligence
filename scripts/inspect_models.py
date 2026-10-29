
import joblib
from pathlib import Path

for path in Path("models").glob("*.joblib"):
    try:
        obj = joblib.load(path)

        print(f"\nFile: {path.name}")
        print(f"Type: {type(obj).__name__}")
        print(f"Has predict: {hasattr(obj, 'predict')}")
        print(f"Has steps: {hasattr(obj, 'steps')}")

        if hasattr(obj, "steps"):
            print("Pipeline steps:", [name for name, _ in obj.steps])

    except Exception as error:
        print(f"\nFile: {path.name} | Error: {error}")
