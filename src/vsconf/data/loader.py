"""data loader for all json resources."""

import json
from pathlib import Path
from typing import Any


DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


def load(name: str) -> Any:
    filepath = DATA_DIR / f"{name}.json"
    with open(filepath) as f:
        return json.load(f)


def get_messages() -> dict:
    global_data = load("global")
    return {k: v for k, v in global_data.items() if k != "shortcuts"}


def get_paths() -> dict:
    return load("paths")


def get_shortcuts() -> dict:
    global_data = load("global")
    return global_data.get("shortcuts", {})


def get_extensions_list() -> list:
    ext_dir = Path(__file__).parent.parent.parent.parent / "extensions"
    extensions = []
    for json_file in sorted(ext_dir.glob("*.json")):
        with open(json_file) as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("//"):
                    continue
                if line.startswith('"') and line.endswith('"'):
                    extensions.append(line[1:-1])
    return extensions
