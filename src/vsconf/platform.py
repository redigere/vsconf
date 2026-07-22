"""platform detection and path resolution."""

import os
import platform
from pathlib import Path
from typing import Optional

from .data import get_paths


def detect_os() -> str:
    system = platform.system().lower()
    if system not in ("linux", "darwin", "windows"):
        raise OSError(f"unsupported platform: {system}")
    return "linux" if system == "linux" else "macos" if system == "darwin" else "windows"


def _expand(path_str: str) -> Path:
    path_str = path_str.replace("~", str(Path.home()))
    path_str = os.path.expandvars(path_str)
    return Path(path_str)


def get_config_dir() -> Path:
    os_name = detect_os()
    paths = get_paths()
    os_paths = paths[os_name]
    if os_name == "linux":
        snap = _expand(os_paths["snap_path"])
        if snap.exists():
            return snap
    return _expand(os_paths["config_path"])


def get_extensions_dir() -> Optional[Path]:
    os_name = detect_os()
    paths = get_paths()
    for path_str in paths[os_name]["extensions_paths"]:
        expanded = _expand(path_str)
        if expanded.exists():
            return expanded
    return None


def get_platform_config_dir() -> Path:
    os_name = detect_os()
    return Path(__file__).parent.parent.parent / "config" / os_name
