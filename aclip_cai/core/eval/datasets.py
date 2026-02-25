import json
from pathlib import Path


def load_golden_dataset(directory: Path | str) -> list[dict]:
    """Loads all test cases from .json files in a specific golden dataset directory."""
    directory = Path(directory)
    dataset = []

    if not directory.exists() or not directory.is_dir():
        return dataset

    for json_file in directory.glob("*.json"):
        try:
            with open(json_file, encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, dict) and "test_cases" in data:
                    dataset.extend(data["test_cases"])
                elif isinstance(data, list):
                    dataset.extend(data)
                else:
                    dataset.append(data)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")

    return dataset
