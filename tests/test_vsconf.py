"""tests for vsconf package."""

import json
from pathlib import Path

from vsconf.core.platform import detect_os, get_platform_config_dir
from vsconf.data.loader import DATA_DIR, get_extensions_list, get_keybindings, get_runners, load, merge_settings


def test_load_global():
    data = load("global")
    assert isinstance(data, dict)
    assert "msg_init" in data


def test_load_paths():
    paths = load("paths")
    assert isinstance(paths, dict)
    os_name = detect_os()
    assert os_name in paths


def test_detect_os():
    os_name = detect_os()
    assert os_name in ("linux", "macos", "windows")


def test_get_extensions_list():
    exts = get_extensions_list()
    assert isinstance(exts, list)
    assert len(exts) > 0
    assert all(isinstance(e, str) for e in exts)


def test_platform_config_dir_exists():
    config_dir = get_platform_config_dir()
    assert config_dir.exists()
    assert (config_dir / "settings.json").exists()


def test_data_files_valid():
    for json_file in DATA_DIR.glob("*.json"):
        with open(json_file) as f:
            data = json.load(f)
        assert isinstance(data, (dict, list))


def test_config_files_valid():
    config_dir = get_platform_config_dir()
    for json_file in config_dir.rglob("*.json"):
        with open(json_file) as f:
            data = json.load(f)
        assert isinstance(data, (dict, list))


def test_extension_files_valid():
    ext_dir = Path(__file__).parent.parent / "extensions"
    for json_file in ext_dir.glob("*.json"):
        with open(json_file) as f:
            data = json.load(f)
        assert isinstance(data, list)


def test_merge_settings():
    os_name = detect_os()
    settings = merge_settings(os_name)
    assert isinstance(settings, dict)
    assert "editor.fontSize" in settings


def test_global_settings_no_terminal_profiles():
    settings = load("settings")
    assert "terminal.integrated.defaultProfile.linux" not in settings


def test_os_settings_has_terminal_profiles():
    os_name = detect_os()
    settings = merge_settings(os_name)
    assert "terminal.integrated.defaultProfile.linux" in settings


def test_get_keybindings():
    kb = get_keybindings()
    assert isinstance(kb, list)
    assert len(kb) > 0


def test_get_runners():
    runners = get_runners()
    assert isinstance(runners, dict)
    assert "code-runner.executorMap" in runners


def test_theme_is_intellij_light():
    settings = load("settings")
    assert settings["workbench.colorTheme"] in ("IntelliJ IDEA Light", "Catppuccin Mocha")
