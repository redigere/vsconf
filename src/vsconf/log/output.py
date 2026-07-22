"""logging setup driven by messages.json."""

import logging
import sys

from ..data.loader import get_messages

_msgs = get_messages()

logger = logging.getLogger("vsconf")


def setup(level: int = logging.INFO) -> None:
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(handler)
    logger.setLevel(level)


def header(msg: str) -> None:
    logger.info(msg)


def info(msg: str) -> None:
    logger.info(_msgs["info"].format(msg=msg))


def success(msg: str) -> None:
    logger.info(_msgs["success"].format(msg=msg))


def warn(msg: str) -> None:
    logger.warning(_msgs["warn"].format(msg=msg))


def error(msg: str) -> None:
    logger.error(_msgs["error"].format(msg=msg))
    sys.exit(1)
