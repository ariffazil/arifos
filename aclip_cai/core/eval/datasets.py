import json
from pathlib import Path

def load_golden_dataset(directory: Path | str) -> list[dict]:
    """Loads all .json files in a specific golden dataset directory."""
    directory = Path(directory)
    dataset = []
    
    if not directory.exists() or not directory.is_dir():
        return dataset
        
    for json_file in directory.glob("*.json"):
        try:
            with open(json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                dataset.append(data)
        except Exception as e:
            print(f"Error loading {json_file}: {e}")
            
    return dataset
