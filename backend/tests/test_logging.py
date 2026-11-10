import json
import logging

import pytest

from app.logging_config import make_formatter, setup_logging


def test_logs_are_one_json_object_per_line(capsys: pytest.CaptureFixture[str]) -> None:
    setup_logging("INFO")

    logging.getLogger("app").info(
        "request",
        extra={"method": "GET", "path": "/drops", "status": 200, "duration_ms": 1.5},
    )

    line = capsys.readouterr().out.strip().splitlines()[-1]
    entry = json.loads(line)
    assert entry["level"] == "INFO"
    assert entry["logger"] == "app"
    assert entry["message"] == "request"
    assert "timestamp" in entry
    assert entry["method"] == "GET"
    assert entry["path"] == "/drops"
    assert entry["status"] == 200
    assert entry["duration_ms"] == 1.5


def test_each_request_is_logged_with_its_fields(client, caplog: pytest.LogCaptureFixture) -> None:
    with caplog.at_level(logging.INFO, logger="app"):
        client.get("/drops")

    record = [r for r in caplog.records if r.getMessage() == "request"][-1]
    entry = json.loads(make_formatter().format(record))
    assert entry["method"] == "GET"
    assert entry["path"] == "/drops"
    assert entry["status"] == 200
    assert entry["duration_ms"] >= 0
