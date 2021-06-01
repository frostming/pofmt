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
      additional_dependencies: ['pangu']  # for handling Chinese documents
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

## Sample output

```diff
--- Original
+++ Current
@@ -21,49 +21,48 @@
 msgid "Welcome to Flask"
 msgstr "欢迎来到 Flask 的世界"

-msgid "Flask: web development, one "drop" at a time"
+msgid "Flask: web development, one \"drop\" at a time"
 msgstr "Flask： Web 开发，一次一滴"

 #: ../../index.rst:11
 msgid ""
-"Welcome to Flask's documentation. Get started with :doc:`installation` "
-"and then get an overview with the :doc:`quickstart`. There is also a more"
-" detailed :doc:`tutorial/index` that shows how to create a small but "
+"Welcome to Flask's documentation. Get started with :doc:`installation` and"
+" then get an overview with the :doc:`quickstart`. There is also a more "
+"detailed :doc:`tutorial/index` that shows how to create a small but "
 "complete application with Flask. Common patterns are described in the "
 ":doc:`patterns/index` section. The rest of the docs describe each "
 "component of Flask in detail, with a full reference in the :doc:`api` "
 "section."
 msgstr ""
-"欢迎来到Flask的文档。你可以从 :doc:`installation` 入手，然后阅读:doc:`quickstart`来了解基本概念。还有一个包含更多细节的:doc:`tutorial/index`"
-"介绍如何用Flask创建一个很小但是完整的程序。一般的开发模式可以在:doc:`patterns/index`章节找到。剩下的文档详细的介绍了Flask的每一个组成部件，"
-"其中:doc:`api`章节包括完整的API参考信息。"
+"欢迎来到 Flask 的文档。你可以从 :doc:`installation` 入手，然后阅读:doc:`quickstart` "
+"来了解基本概念。还有一个包含更多细节的:doc:`tutorial/index` 介绍如何用 Flask "
+"创建一个很小但是完整的程序。一般的开发模式可以在:doc:`patterns/index` 章节找到。剩下的文档详细的介绍了 Flask "
+"的每一个组成部件，其中:doc:`api` 章节包括完整的 API 参考信息。"

 #: ../../index.rst:19
-msgid "Flask depends on the `Jinja`_ template engine and the `Werkzeug`_ WSGI toolkit. The documentation for these libraries can be found at:"
-msgstr ""
-"Flask 依赖 `Jinja`_ 模板引擎和 `Werkzeug`_ WSGI 工具集。这些库的文档如下："
+msgid ""
+"Flask depends on the `Jinja`_ template engine and the `Werkzeug`_ WSGI "
+"toolkit. The documentation for these libraries can be found at:"
+msgstr "Flask 依赖 `Jinja`_ 模板引擎和 `Werkzeug`_ WSGI 工具集。这些库的文档如下："

 #: ../../index.rst:22
 msgid "`Jinja documentation <https://jinja.palletsprojects.com/>`_"
-msgstr "`Jinja文档<https://jinja.palletsprojects.com/>`_"
+msgstr "`Jinja 文档 <https://jinja.palletsprojects.com/>`_"

 #: ../../index.rst:23
 msgid "`Werkzeug documentation <https://werkzeug.palletsprojects.com/>`_"
-msgstr "`Werkzeug文档<https://werkzeug.palletsprojects.com/>`_"
+msgstr "`Werkzeug 文档 <https://werkzeug.palletsprojects.com/>`_"

 #: ../../index.rst:30
 msgid "User's Guide"
-msgstr ""
-"用户指南"
+msgstr "用户指南"

 #: ../../index.rst:32
 msgid ""
 "This part of the documentation, which is mostly prose, begins with some "
 "background information about Flask, then focuses on step-by-step "
 "instructions for web development with Flask."
-msgstr ""
-"这部分的文档大部分是独立章节，以一些关于 Flask 的背景信息开始，然后重点介绍如何"
-"使用 Flask 一步步进行 Web 开发。"
+msgstr "这部分的文档大部分是独立章节，以一些关于 Flask 的背景信息开始，然后重点介绍如何使用 Flask 一步步进行 Web 开发。"

 #: ../../index.rst:66
 msgid "API Reference"
@@ -73,13 +72,13 @@
 msgid ""
 "If you are looking for information on a specific function, class or "
 "method, this part of the documentation is for you."
-msgstr ""
-"如果你想找关于某个特定函数、类或方法的信息，那么这部分文档就是为你准备的。"
+msgstr "如果你想找关于某个特定函数、类或方法的信息，那么这部分文档就是为你准备的。"

 #: ../../index.rst:78
 msgid "Additional Notes"
 msgstr "附加笔记"

 #: ../../index.rst:80
-msgid "Design notes, legal information and changelog are here for the interested."
+msgid ""
+"Design notes, legal information and changelog are here for the interested."
 msgstr "如果你感兴趣的话，这里有一些设计笔记、法律信息和变更日志（changelog）。"
```
