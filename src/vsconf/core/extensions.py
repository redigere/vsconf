"""extension management."""

import json
import logging
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path
from typing import Optional

from ..data.loader import get_extensions_list

logger = logging.getLogger("vsconf")

OPEN_VSX_API = "https://open-vsx.org/api/{publisher}/{name}"
_EXTENSIONS_DIR = Path(__file__).parent.parent.parent.parent / "extensions"
_TIMEOUT = 30


def load() -> list[str]:
    return get_extensions_list()


def _run_code(*args: str) -> Optional[subprocess.CompletedProcess[str]]:
    try:
        return subprocess.run(["code", *args], capture_output=True, text=True, check=False)
    except FileNotFoundError:
        logger.warning("'code' command not found")
        return None


def get_installed() -> set[str]:
    result = _run_code("--list-extensions")
    if result is None:
        return set()
    return {ext.lower() for ext in result.stdout.strip().splitlines() if ext}


def _split_id(ext_id: str) -> tuple[str, str]:
    publisher, _, name = ext_id.partition(".")
    return publisher, name


def _cache_dir() -> Path:
    base = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache"))
    return base / "vsconf"


def _download_vsix(ext_id: str) -> Optional[Path]:
    publisher, name = _split_id(ext_id)
    api_url = OPEN_VSX_API.format(publisher=publisher, name=name)
    try:
        with urllib.request.urlopen(api_url, timeout=_TIMEOUT) as resp:
            meta = json.load(resp)
    except (urllib.error.URLError, urllib.error.HTTPError, OSError, ValueError) as e:
        logger.warning(f"open-vsx unavailable for {ext_id}: {e}")
        return None

    version = meta.get("version")
    download_url = (meta.get("files") or {}).get("download")
    if not version or not download_url:
        logger.warning(f"no downloadable vsix for {ext_id} on open-vsx")
        return None

    cache = _cache_dir()
    cache.mkdir(parents=True, exist_ok=True)
    vsix_path = cache / f"{ext_id.replace('/', '_')}-{version}.vsix"
    if vsix_path.exists():
        return vsix_path

    try:
        with urllib.request.urlopen(download_url, timeout=_TIMEOUT) as resp:
            data = resp.read()
    except (urllib.error.URLError, urllib.error.HTTPError, OSError) as e:
        logger.warning(f"failed to download {download_url}: {e}")
        return None

    vsix_path.write_bytes(data)
    return vsix_path


def _local_vsix(ext_id: str) -> Path:
    return _EXTENSIONS_DIR / f"{ext_id}.vsix"


def install_one(ext_id: str) -> bool:
    vsix_path = _download_vsix(ext_id)
    if vsix_path is None:
        local = _local_vsix(ext_id)
        if not local.exists():
            logger.warning(f"vsix not found for {ext_id} (open-vsx and {local.name})")
            return False
        vsix_path = local
    result = _run_code("--install-extension", str(vsix_path), "--force")
    if result is None:
        return False
    if result.returncode == 0:
        logger.info(f"installed: {ext_id}")
        return True
    logger.warning(f"failed: {ext_id}: {result.stderr.strip()}")
    return False


def uninstall_one(ext_id: str) -> bool:
    result = _run_code("--uninstall-extension", ext_id)
    if result is None:
        return False
    if result.returncode == 0:
        logger.info(f"removed: {ext_id}")
        return True
    logger.warning(f"failed to remove {ext_id}: {result.stderr.strip()}")
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
