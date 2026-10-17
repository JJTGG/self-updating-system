import requests

def fetch_json(url: str, timeout: int = 30) -> dict:
    response = requests.get(url, timeout=timeout, headers={"Accept": "application/vnd.github+json"})
    response.raise_for_status()
    return response.json()
