import hashlib, json
from datetime import datetime, timezone
from pathlib import Path

def update_outputs(payload: dict, output_dir: str, latest_path: str, snapshots_dir: str) -> dict:
    root = Path(output_dir)
    latest = Path(latest_path)
    snapshots = Path(snapshots_dir)
    for directory in (root, latest.parent, snapshots):
        directory.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc)
    stamp = now.strftime("%Y%m%dT%H%M%SZ")
    snapshot = snapshots / f"{stamp}.json"
    serialized = json.dumps(payload, indent=2, ensure_ascii=False)
    snapshot.write_text(serialized, encoding="utf-8")
    latest.write_text(serialized, encoding="utf-8")
    return {
        "updated_at": now.isoformat(),
        "snapshot": str(snapshot),
        "latest": str(latest),
        "content_hash": hashlib.sha256(serialized.encode()).hexdigest(),
    }
