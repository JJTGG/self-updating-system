import json
from app.validator import validate_payload, ValidationError
from app.updater import update_outputs
from app.changelog import append_entry

def test_validator_accepts_valid_payload():
    payload = {"full_name": "test", "html_url": "https://example.com"}
    assert validate_payload(payload, ["full_name", "html_url"], 1000) == payload

def test_validator_rejects_missing_fields():
    try:
        validate_payload({}, ["full_name"], 1000)
    except ValidationError as exc:
        assert "full_name" in str(exc)
    else:
        raise AssertionError("Expected ValidationError")

def test_updater_writes_latest_and_snapshot(tmp_path):
    result = update_outputs({"ok": True}, str(tmp_path), str(tmp_path/"latest.json"), str(tmp_path/"snapshots"))
    assert (tmp_path/"latest.json").exists()
    assert result["content_hash"]

def test_changelog_appends(tmp_path):
    path = tmp_path/"CHANGELOG.md"
    append_entry(str(path), {"updated_at":"now","snapshot":"x","content_hash":"abc"})
    text = path.read_text()
    assert "success" in text and "abc" in text
