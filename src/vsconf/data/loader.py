"""data loader for all json resources."""

import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


def load(name: str) -> Any:
    filepath = DATA_DIR / f"{name}.json"
    try:
        with open(filepath) as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"data file not found: {filepath}") from None
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid JSON in {filepath}: {e}") from e


def get_messages() -> dict[str, Any]:
    global_data = load("global")
    return {k: v for k, v in global_data.items() if k != "shortcuts"}


def get_paths() -> dict[str, Any]:
    return load("paths")  # type: ignore[no-any-return]


def get_shortcuts() -> dict[str, Any]:
    global_data = load("global")
    return global_data.get("shortcuts", {})  # type: ignore[no-any-return]


def get_extensions_list() -> list[str]:
    ext_dir = Path(__file__).parent.parent.parent.parent / "extensions"
    extensions: list[str] = []
    for json_file in sorted(ext_dir.glob("*.json")):
        with open(json_file) as f:
            extensions.extend(json.load(f))
    return extensions
