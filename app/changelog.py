from datetime import datetime, timezone
from pathlib import Path

def append_entry(path: str, result: dict, status: str = "success", notes: str = "") -> None:
    file = Path(path)
    file.parent.mkdir(parents=True, exist_ok=True)
    if not file.exists():
        file.write_text("# Changelog\n\nAll automated updates, validations, and repairs.\n\n", encoding="utf-8")
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    entry = f"## {stamp} — {status}\n\n- Updated at: {result.get('updated_at', 'n/a')}\n- Snapshot: `{result.get('snapshot', 'n/a')}`\n- Content hash: `{result.get('content_hash', 'n/a')}`\n"
    if notes:
        entry += f"- Notes: {notes}\n"
    with file.open("a", encoding="utf-8") as f:
        f.write(entry + "\n")
