"""security audit."""

from pathlib import Path

from .extensions import uninstall_one
from .platform import get_config_dir, get_extensions_dir


def _check(filepath: Path, pattern: str) -> bool:
    if not filepath.exists():
        return False
    return pattern in filepath.read_text()


def audit() -> dict:
    settings = get_config_dir() / "settings.json"
    return {
        "marketplace_blocked": _check(settings, "127.0.0.1:65535"),
        "telemetry_off": _check(settings, '"telemetry.telemetryLevel": "off"'),
        "copilot_disabled": _check(settings, '"github.copilot.enable"'),
        "agents_disabled": _check(settings, '"workbench.agent.enabled": false'),
    }


def enforce_publishers(installed: set[str], desired: list[str]) -> list[str]:
    ext_dir = get_extensions_dir()
    if not ext_dir:
        return []
    desired_lower = {ext.lower() for ext in desired}
    to_remove = []
    for ext in installed:
        if ext not in desired_lower:
            to_remove.append(ext)
            continue
        matches = list(ext_dir.glob(f"{ext}-*"))
        if matches:
            manifest = matches[0] / ".vsixmanifest"
            if manifest.exists() and "unverified" in manifest.read_text().lower():
                to_remove.append(ext)
    for ext in to_remove:
        uninstall_one(ext)
    return to_remove
