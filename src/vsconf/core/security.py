"""security audit."""

from pathlib import Path

from .platform import get_config_dir


def _check(filepath: Path, pattern: str) -> bool:
    if not filepath.exists():
        return False
    try:
        return pattern in filepath.read_text()
    except OSError:
        return False


def audit() -> dict[str, bool]:
    settings = get_config_dir() / "settings.json"
    return {
        "telemetry_off": _check(settings, '"telemetry.telemetryLevel": "off"'),
        "gallery_disabled": _check(settings, '"extensions.gallery.enabled": false'),
        "updates_disabled": _check(settings, '"update.mode": "none"'),
    }
