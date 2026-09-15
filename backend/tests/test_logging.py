import json
import logging

from app.core.logging import JsonFormatter


def test_json_formatter_emits_structured_payload() -> None:
    formatter = JsonFormatter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname=__file__,
        lineno=1,
        msg="startup complete",
        args=(),
        exc_info=None,
    )
    record.request_id = "abc-123"
    payload = json.loads(formatter.format(record))
    assert payload["message"] == "startup complete"
    assert payload["level"] == "INFO"
    assert payload["request_id"] == "abc-123"
    assert "timestamp" in payload
