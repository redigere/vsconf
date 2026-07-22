"""runner configuration."""

import json
from pathlib import Path
from typing import Optional

from .platform import get_platform_config_dir


def load_config() -> Optional[dict]:
    path = get_platform_config_dir() / "runners.json"
    if not path.exists():
        return None
    try:
        with open(path) as f:
            return json.load(f)
    except json.JSONDecodeError:
        return None


def is_valid() -> bool:
    return load_config() is not None
