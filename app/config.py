import json, os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def load_config(path: str = "config/system.json") -> dict:
    with open(ROOT / path, encoding="utf-8") as f:
        return json.load(f)

def source_url(config: dict) -> str:
    env_name = config["source"]["url_env"]
    url = os.getenv(env_name)
    if not url:
        raise ValueError(f"Missing environment variable: {env_name}")
    return url
