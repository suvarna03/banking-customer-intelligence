
from pathlib import Path
import shutil

PROJECT_ROOT = Path(__file__).resolve().parent.parent

PROCESSED_DIR = PROJECT_ROOT / "data" / "processed"
ARTIFACTS_DIR = PROJECT_ROOT / "artifacts"

phase_folders = {
    "phase_1": ARTIFACTS_DIR / "phase_1",
    "phase_2": ARTIFACTS_DIR / "phase_2",
    "phase_3": ARTIFACTS_DIR / "phase_3",
    "phase_4": ARTIFACTS_DIR / "phase_4",
}

for folder in phase_folders.values():
    folder.mkdir(parents=True, exist_ok=True)

if PROCESSED_DIR.exists():
    for file_path in PROCESSED_DIR.iterdir():
        if not file_path.is_file():
            continue

        filename = file_path.name

        if filename in {
            "banking77_train_eda.csv",
            "phase1_dataset_report.csv",
        }:
            destination = phase_folders["phase_1"] / filename

        elif filename == "phase2_top_terms.csv":
            destination = phase_folders["phase_2"] / filename

        elif filename.startswith("phase3_"):
            destination = phase_folders["phase_3"] / filename

        else:
            destination = phase_folders["phase_4"] / filename

        if destination.exists():
            print(f"Skipped existing file: {destination}")
            continue

        shutil.move(str(file_path), str(destination))
        print(f"Moved: {filename} -> {destination.relative_to(PROJECT_ROOT)}")

print("\nArtifact organization completed.")
