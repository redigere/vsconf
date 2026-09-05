"""cli entry point."""

import argparse
import sys

from .. import __version__
from ..core.extensions import get_installed, install, load, purge
from ..core.platform import detect_os
from ..core.security import audit
from ..core.settings import write_all
from ..data.loader import get_ansi, get_runners, get_tiling
from ..log.output import header, info, logger, msg, setup, success, warn


def cmd_install(args: argparse.Namespace) -> None:
    os_name = detect_os()
    header(f"vsconf ({os_name})")
    info(msg("msg_init"))

    desired = load()
    info(msg("msg_loaded", count=len(desired)))

    installed = get_installed()
    removed = purge(installed, desired)
    if removed:
        info(msg("msg_purged", count=len(removed)))

    installed = get_installed()
    new = install(desired, installed)
    if new:
        info(msg("msg_installed", count=len(new)))

    config = write_all()
    success(msg("msg_settings_written", path=config["settings"]))

    sec = audit()
    for check, passed in sec.items():
        label = "ok" if passed else "fail"
        info(f"  {check}: {label}")

    runners = get_runners()
    if runners.get("code-runner.executorMap"):
        success(msg("msg_runners_valid"))

    installed = get_installed()
    found = sum(1 for ext in desired if ext.lower() in installed)
    info(msg("msg_installed_status", found=found, total=len(desired)))

    success(msg("msg_complete"))


def cmd_extensions(args: argparse.Namespace) -> None:
    header("extensions")
    desired = load()
    installed = get_installed()
    removed = purge(installed, desired)
    if removed:
        info(msg("msg_purged", count=len(removed)))
    installed = get_installed()
    new = install(desired, installed)
    if new:
        info(msg("msg_installed", count=len(new)))


def cmd_settings(args: argparse.Namespace) -> None:
    header("settings")
    config = write_all()
    success(msg("msg_settings_written", path=config["settings"]))
    sec = audit()
    for check, passed in sec.items():
        label = "ok" if passed else "fail"
        info(f"  {check}: {label}")


def cmd_security(args: argparse.Namespace) -> None:
    header("security")
    sec = audit()
    for check, passed in sec.items():
        label = "ok" if passed else "fail"
        info(f"  {check}: {label}")
    if not all(sec.values()):
        sys.exit(1)


def cmd_list(args: argparse.Namespace) -> None:
    header("extension list")
    desired = load()
    ansi = get_ansi()
    tiling = get_tiling()

    blue = ansi.get("blue", "")
    teal = ansi.get("teal", "")
    dim = ansi.get("dim", "")
    reset = ansi.get("reset", "")

    fixed_rows = tiling.get("fixed_rows", 3)
    max_col_width = tiling.get("col_width", 40)
    line_width = tiling.get("line_width", 78)

    cols = max(1, (len(desired) + fixed_rows - 1) // fixed_rows) if desired else 1
    col_width = max((len(ext) for ext in desired), default=0) if desired else 0
    col_width = min(col_width, max_col_width) + 3

    logger.info("")
    logger.info(f"  {blue}{'─' * line_width}{reset}")
    logger.info(f"  {blue} TILING LAYOUT {dim}│ {teal}rows: {fixed_rows} {dim}│ cols: {cols} {dim}│ total: {len(desired)}{reset}")
    logger.info(f"  {blue}{'─' * line_width}{reset}")
    logger.info("")

    for row in range(fixed_rows):
        parts = []
        for col in range(cols):
            idx = row + col * fixed_rows
            if idx < len(desired):
                ext = desired[idx]
                cell = f"{teal}{idx + 1:3d}.{reset} {ext}"
                parts.append(cell.ljust(col_width + 12))
            else:
                parts.append("".ljust(col_width + 12))
        logger.info("    " + "  ".join(parts))

    logger.info("")
    logger.info(f"  {blue}{'─' * line_width}{reset}")
    info(msg("msg_total", count=len(desired)))


def cmd_status(args: argparse.Namespace) -> None:
    header("status")
    desired = load()
    installed = get_installed()
    found = sum(1 for ext in desired if ext.lower() in installed)
    missing = len(desired) - found
    info(msg("msg_installed_status", found=found, total=len(desired)))
    if missing > 0:
        warn(msg("msg_missing", count=missing))


def cmd_runners(args: argparse.Namespace) -> None:
    header("runners")
    runners = get_runners()
    executor_map = runners.get("code-runner.executorMap", {})
    for lang, cmd in sorted(executor_map.items()):
        logger.info(f"  {lang}: {cmd}")


def cmd_uninstall(args: argparse.Namespace) -> None:
    header("purge")
    desired = load()
    installed = get_installed()
    removed = purge(installed, desired)
    success(msg("msg_purge_done", count=len(removed)))


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
