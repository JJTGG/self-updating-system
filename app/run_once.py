import sys
from app.config import load_config, source_url
from app.fetcher import fetch_json
from app.validator import validate_payload, ValidationError
from app.updater import update_outputs
from app.changelog import append_entry

def main() -> int:
    config = load_config()
    try:
        payload = fetch_json(source_url(config), config["source"]["timeout_seconds"])
        payload = validate_payload(payload, config["validation"]["required_fields"], config["validation"]["max_response_bytes"])
        result = update_outputs(payload, config["output"]["dir"], config["output"]["latest"], config["output"]["snapshots"])
        append_entry(config["changelog"], result)
        print(f"Update succeeded: {result['content_hash']}")
        return 0
    except Exception as exc:
        append_entry(config["changelog"], {}, status="failure", notes=repr(exc))
        print(f"Update failed: {exc}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
