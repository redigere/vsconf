# vsconf

cross platform provisioning for vs code. pure code, no ai.

## install

    pip install vsconf

from source:

    git clone https://github.com/redigere/vsconf.git
    cd vsconf
    pip install -e .

## usage

    vsconf install       full installation
    vsconf extensions    install extensions only
    vsconf settings      write settings only
    vsconf security      run security audit
    vsconf list          list all extensions
    vsconf status        show installation status
    vsconf runners       show runner commands
    vsconf uninstall     remove non-whitelisted extensions

## what it does

reads platform config from data/paths.json. writes vs code settings, keybindings, snippets from config/{linux,macos,windows}/. manages extensions from extensions/*.json. runs security audit checking marketplace block, telemetry, copilot, agents.

## structure

    src/vsconf/     python package
    data/           json resources (messages, paths, shortcuts)
    config/         platform settings, keybindings, snippets
    extensions/     extension whitelist by category
    tests/          pytest suite

## ci

github actions runs lint (ruff, mypy), tests (pytest on 3 os, 4 python versions), and json validation on push/pr to main.

## license

gpl-3.0
