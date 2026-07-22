"""extension management."""

import subprocess

from ..data.loader import get_extensions_list


def load() -> list[str]:
    return get_extensions_list()


def get_installed() -> set[str]:
    try:
        result = subprocess.run(
            ["code", "--list-extensions"], capture_output=True, text=True, check=False
        )
        return {ext.lower() for ext in result.stdout.strip().splitlines() if ext}
    except FileNotFoundError:
        return set()


def install_one(ext_id: str) -> bool:
    try:
        subprocess.run(
            ["code", "--install-extension", ext_id, "--force"], capture_output=True, check=True
        )
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def uninstall_one(ext_id: str) -> bool:
    try:
        subprocess.run(["code", "--uninstall-extension", ext_id], capture_output=True, check=True)
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False


def purge(installed: set[str], desired: list[str]) -> list[str]:
    desired_lower = {ext.lower() for ext in desired}
    removed = [ext for ext in installed if ext not in desired_lower]
    for ext in removed:
        uninstall_one(ext)
    return removed


def install(desired: list[str], installed: set[str]) -> list[str]:
    installed_new = []
    for ext in desired:
        if ext.lower() not in installed and install_one(ext):
            installed_new.append(ext)
    return installed_new
