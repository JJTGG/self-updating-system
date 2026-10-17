from typing import Any

class ValidationError(Exception):
    pass

def validate_payload(payload: Any, required_fields: list[str], max_bytes: int) -> dict:
    if not isinstance(payload, dict):
        raise ValidationError("Expected a JSON object")
    missing = [field for field in required_fields if field not in payload]
    if missing:
        raise ValidationError(f"Missing required fields: {', '.join(missing)}")
    size = len(str(payload).encode("utf-8"))
    if size > max_bytes:
        raise ValidationError(f"Payload too large: {size} bytes")
    return payload
