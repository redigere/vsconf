"""extension management."""

import logging
import subprocess
from typing import Optional

from ..data.loader import get_extensions_list

logger = logging.getLogger("vsconf")


def load() -> list[str]:
    return get_extensions_list()


def _run_code(*args: str) -> Optional[subprocess.CompletedProcess[str]]:
    try:
        return subprocess.run(["code", *args], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        logger.warning("'code' command not found. Skipping extension operation.")
        return None


def get_installed() -> set[str]:
    result = _run_code("--list-extensions")
    if result is None:
        return set()
    return {ext.lower() for ext in result.stdout.strip().splitlines() if ext}


def install_one(ext_id: str) -> bool:
    result = _run_code("--install-extension", ext_id, "--force")
    if result is None:
        return False
    if result.returncode == 0:
        logger.info(f"installed: {ext_id}")
        return True
    logger.warning(f"failed to install {ext_id}: {result.stderr.strip()}")
    return False


def uninstall_one(ext_id: str) -> bool:
    result = _run_code("--uninstall-extension", ext_id)
    if result is None:
        return False
    if result.returncode == 0:
        logger.info(f"uninstalled: {ext_id}")
        return True
    logger.warning(f"failed to uninstall {ext_id}: {result.stderr.strip()}")
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
