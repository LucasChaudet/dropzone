"""Logs on stdout, in JSON: one object per line and per event."""

import logging
import sys

from pythonjsonlogger.core import RESERVED_ATTRS
from pythonjsonlogger.json import JsonFormatter


def make_formatter() -> JsonFormatter:
    """Fields of every line: timestamp, level, logger, message, plus the `extra=` fields
    (for each request: method, path, status, duration_ms)."""
    return JsonFormatter(
        "{levelname}{name}{message}",
        style="{",
        rename_fields={"levelname": "level", "name": "logger"},
        timestamp=True,
        # Uvicorn adds a colored copy of its messages: useless in JSON.
        reserved_attrs=[*RESERVED_ATTRS, "color_message"],
        json_ensure_ascii=False,
    )


def setup_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(make_formatter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level.upper())
    # Uvicorn's own loggers go through the root handler.
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        uvicorn_logger = logging.getLogger(name)
        uvicorn_logger.handlers = []
        uvicorn_logger.propagate = True
    # Access logs are written by our middleware, with the request duration.
    logging.getLogger("uvicorn.access").disabled = True
