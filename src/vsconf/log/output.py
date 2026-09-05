"""logging setup with structured output."""

import logging
import sys
from enum import Enum

from ..data.loader import get_messages


class Level(Enum):
    INFO = "info"
    SUCCESS = "success"
    WARN = "warn"
    ERROR = "error"


_COLORS = {
    Level.INFO: "\033[36m",
    Level.SUCCESS: "\033[32m",
    Level.WARN: "\033[33m",
    Level.ERROR: "\033[31m",
}

_RESET = "\033[0m"
_BOLD = "\033[1m"
_DIM = "\033[2m"

_PREFIXES = {
    Level.INFO: "  ",
    Level.SUCCESS: "+ ",
    Level.WARN: "! ",
    Level.ERROR: "x ",
}


class _Formatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return record.getMessage()


logger = logging.getLogger("vsconf")
_msgs: dict[str, str] = {}


def setup(level: int = logging.INFO) -> None:
    global _msgs
    _msgs = get_messages()

    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(_Formatter())
    logger.addHandler(handler)
    logger.setLevel(level)


def _emit(level: Level, msg: str) -> None:
    color = _COLORS[level]
    prefix = _PREFIXES[level]
    logger.log(
        logging.WARNING if level in (Level.WARN, Level.ERROR) else logging.INFO,
        f"{color}{prefix}{msg}{_RESET}",
    )


def header(msg: str) -> None:
    logger.info(f"{_BOLD}{msg}{_RESET}")


def info(msg: str) -> None:
    _emit(Level.INFO, msg)


def success(msg: str) -> None:
    _emit(Level.SUCCESS, msg)


def warn(msg: str) -> None:
    _emit(Level.WARN, msg)


def error(msg: str) -> None:
    _emit(Level.ERROR, msg)
    sys.exit(1)


def msg(key: str, **kwargs: object) -> str:
    template = _msgs.get(key, key)
    return template.format(**kwargs) if kwargs else template
