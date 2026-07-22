"""settings, keybindings, snippets."""

import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

from .platform import get_config_dir, get_platform_config_dir


def _backup(filepath: Path) -> Optional[Path]:
    if filepath.exists():
        backup = filepath.with_suffix(f".bak-{int(datetime.now().timestamp())}")
        shutil.copy2(filepath, backup)
        return backup
    return None


def _copy(src: Path, dst: Path) -> Path:
    dst.parent.mkdir(parents=True, exist_ok=True)
    _backup(dst)
    shutil.copy2(src, dst)
    return dst


def write_settings() -> Path:
    src = get_platform_config_dir() / "settings.json"
    dst = get_config_dir() / "settings.json"
    return _copy(src, dst)


def write_keybindings() -> Path:
    src = get_platform_config_dir() / "keybindings.json"
    dst = get_config_dir() / "keybindings.json"
    return _copy(src, dst)


def write_snippets() -> Path:
    src_dir = get_platform_config_dir() / "snippets"
    dst_dir = get_config_dir() / "snippets"
    if src_dir.exists():
        dst_dir.mkdir(parents=True, exist_ok=True)
        for f in src_dir.glob("*.json"):
            shutil.copy2(f, dst_dir / f.name)
    return dst_dir


def write_all() -> dict:
    return {
        "settings": write_settings(),
        "keybindings": write_keybindings(),
        "snippets": write_snippets(),
    }
