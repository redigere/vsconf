"""cli entry point."""

import argparse
import sys

from .. import __version__
from ..core.extensions import get_installed, install, load, purge
from ..core.platform import detect_os
from ..core.runners import is_valid
from ..core.security import audit
from ..core.settings import write_all
from ..data.loader import get_messages, get_shortcuts
from ..log.output import header, info, logger, setup, success, warn

_msgs = get_messages()


def cmd_install(args: argparse.Namespace) -> None:
    os_name = detect_os()
    header(f"{_msgs['header_install']} ({os_name})")
    info(_msgs["msg_init"])

    desired = load()
    info(_msgs["msg_loaded"].format(count=len(desired)))

    installed = get_installed()
    removed = purge(installed, desired)
    if removed:
        info(_msgs["msg_purged"].format(count=len(removed)))

    installed = get_installed()
    new = install(desired, installed)
    if new:
        info(_msgs["msg_installed"].format(count=len(new)))

    config = write_all()
    success(_msgs["msg_settings_written"].format(path=config["settings"]))

    sec = audit()
    for check, passed in sec.items():
        label = _msgs["check_ok"] if passed else _msgs["check_fail"]
        info(f"{check}: {label}")

    if is_valid():
        success(_msgs["msg_runners_valid"])

    shortcuts = get_shortcuts()
    header(_msgs["header_runners"])
    for key, val in shortcuts.items():
        logger.info(f"  {key}: {val}")

    installed = get_installed()
    found = sum(1 for ext in desired if ext.lower() in installed)
    info(_msgs["msg_installed_status"].format(found=found, total=len(desired)))

    success(_msgs["msg_complete"])


def cmd_extensions(args: argparse.Namespace) -> None:
    header(_msgs["header_extensions"])
    desired = load()
    installed = get_installed()
    removed = purge(installed, desired)
    if removed:
        info(_msgs["msg_purged"].format(count=len(removed)))
    installed = get_installed()
    new = install(desired, installed)
    if new:
        info(_msgs["msg_installed"].format(count=len(new)))


def cmd_settings(args: argparse.Namespace) -> None:
    header(_msgs["header_settings"])
    config = write_all()
    success(_msgs["msg_settings_written"].format(path=config["settings"]))
    sec = audit()
    for check, passed in sec.items():
        label = _msgs["check_ok"] if passed else _msgs["check_fail"]
        info(f"{check}: {label}")


def cmd_security(args: argparse.Namespace) -> None:
    header(_msgs["header_security"])
    sec = audit()
    for check, passed in sec.items():
        label = _msgs["check_ok"] if passed else _msgs["check_fail"]
        info(f"{check}: {label}")
    if not all(sec.values()):
        sys.exit(1)


def cmd_list(args: argparse.Namespace) -> None:
    header(_msgs["header_list"])
    desired = load()
    for i, ext in enumerate(desired, 1):
        logger.info(f"  {i:3d}. {ext}")
    info(_msgs["msg_total"].format(count=len(desired)))


def cmd_status(args: argparse.Namespace) -> None:
    header(_msgs["header_status"])
    desired = load()
    installed = get_installed()
    found = sum(1 for ext in desired if ext.lower() in installed)
    missing = len(desired) - found
    info(_msgs["msg_installed_status"].format(found=found, total=len(desired)))
    if missing > 0:
        warn(_msgs["msg_missing"].format(count=missing))


def cmd_runners(args: argparse.Namespace) -> None:
    header(_msgs["header_runners"])
    shortcuts = get_shortcuts()
    for key, val in shortcuts.items():
        logger.info(f"  {key}: {val}")


def cmd_uninstall(args: argparse.Namespace) -> None:
    header(_msgs["header_uninstall"])
    desired = load()
    installed = get_installed()
    removed = purge(installed, desired)
    success(_msgs["msg_purge_done"].format(count=len(removed)))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="vsconf", description="vs code pure code setup")
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = parser.add_subparsers(dest="command")
    sub.add_parser("install", help="full installation")
    sub.add_parser("extensions", help="install extensions only")
    sub.add_parser("settings", help="write settings only")
    sub.add_parser("security", help="run security audit")
    sub.add_parser("list", help="list all extensions")
    sub.add_parser("status", help="show installation status")
    sub.add_parser("runners", help="show runner commands")
    sub.add_parser("uninstall", help="remove non-whitelisted extensions")
    return parser


def main(argv: list[str] | None = None) -> None:
    setup()
    parser = build_parser()
    args = parser.parse_args(argv)
    commands = {
        "install": cmd_install,
        "extensions": cmd_extensions,
        "settings": cmd_settings,
        "security": cmd_security,
        "list": cmd_list,
        "status": cmd_status,
        "runners": cmd_runners,
        "uninstall": cmd_uninstall,
    }
    if args.command is None:
        parser.print_help()
        sys.exit(0)
    commands[args.command](args)
