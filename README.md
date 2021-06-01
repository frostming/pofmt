# pofmt

[![Tests](https://github.com/frostming/pofmt/workflows/Tests/badge.svg)](https://github.com/frostming/pofmt/actions?query=workflow%3Aci)
[![pypi version](https://img.shields.io/pypi/v/pofmt.svg)](https://pypi.org/project/pofmt/)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

Your missing PO formatter and linter

## Features

- Wrap msgid and msgstr with a constant max width.
- Can act as a [pre-commit](https://pre-commit.com/) hook.
- Display lint errors in a human readable format.
- Insert white-spaces between Chinese characters and latin letters with [pangu](https://github.com/vinta/pangu.py)

## Requirements

pofmt requires Python >=3.6

## Installation

It is recommended to install with `pipx`, if `pipx` haven't been installed yet, refer to the [pipx's docs](https://github.com/pipxproject/pipx)

```bash
$ pipx install pofmt
```

Alternatively, install with `pip` to the user site:

```bash
$ python -m pip install --user pofmt
```

If you are formatting PO files with Chinese, it is recommended to install `pofmt[zh]`. This includes
a handy function to add spaces between CJK characters and latin letters.

## As a pre-commit hook

See [pre-commit](https://pre-commit.com/) for instructions.

A sample `.pre-commit-config.yaml`:

```yaml
- repo: https://github.com/frostming/pofmt
  rev: '0.1.0'
  hooks:
    - id: pofmt
```

## Usage

```
USAGE: pofmt [-h] [--line-length LINE_LENGTH] [-c] [filename ...]
       python -m pofmt [-h] [--line-length LINE_LENGTH] [-c] [filename ...]

Format PO files for consistency

positional arguments:
  filename              Filenames to format, default to all po files under the current directory(recursively)

optional arguments:
  -h, --help            show this help message and exit
  --line-length LINE_LENGTH
                        The max length of msgid and msgstr
  -c, --check           Check only, don't modify files
```
