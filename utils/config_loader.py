import yaml
from pathlib import Path

def load_prompts() -> dict:
    file_path = Path(__file__).parent.parent / "prompts.yaml"
    try:
        with open(Path(file_path), "r") as file:
            return yaml.safe_load(file) or {}
    except FileNotFoundError:
        raise FileNotFoundError(f"Prompts file {file_path} not found")
    except yaml.YAMLError as e:
        raise yaml.YAMLError(f"Error parsing YAML file: {e}")