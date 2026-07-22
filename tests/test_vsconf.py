"""Tests for vsconf package."""

import json
from pathlib import Path

import pytest

from vsconf.data import load, get_extensions_list, DATA_DIR
from vsconf.platform import detect_os, get_platform_config_dir


def test_load_messages():
    msg = load("messages")
    assert isinstance(msg, dict)
    assert "info" in msg
    assert "success" in msg


def test_load_paths():
    paths = load("paths")
    assert isinstance(paths, dict)
    os_name = detect_os()
    assert os_name in paths


def test_load_shortcuts():
    sc = load("shortcuts")
    assert isinstance(sc, dict)
    assert "run_file" in sc


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
