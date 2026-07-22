"""extension management."""

import subprocess
from typing import List, Set

from ..data.loader import get_extensions_list
from .platform import get_extensions_dir


def load() -> List[str]:
    return get_extensions_list()


def get_installed() -> Set[str]:
    try:
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True,
            text=True,
            check=False
        )
        return {ext.lower() for ext in result.stdout.strip().splitlines() if ext}
    except FileNotFoundError:
        return set()


def install_one(ext_id: str) -> bool:
    try:
        subprocess.run(
            ["code", "--install-extension", ext_id, "--force"],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def uninstall_one(ext_id: str) -> bool:
    try:
        subprocess.run(
            ["code", "--uninstall-extension", ext_id],
            capture_output=True,
            check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def purge(installed: Set[str], desired: List[str]) -> List[str]:
    desired_lower = {ext.lower() for ext in desired}
    removed = [ext for ext in installed if ext not in desired_lower]
    for ext in removed:
        uninstall_one(ext)
    return removed


def install(desired: List[str], installed: Set[str]) -> List[str]:
    installed_new = []
    for ext in desired:
        if ext.lower() not in installed:
            if install_one(ext):
                installed_new.append(ext)
    return installed_new
