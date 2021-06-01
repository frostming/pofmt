import argparse
import codecs
import difflib
import glob
import locale
import os
import re
import sys
import textwrap
import typing as t
from pathlib import Path

try:
    import pangu
except ModuleNotFoundError:
    pangu = None

MESSAGE_RE = r'"(.*)"[ ]*$'


class ParseError(Exception):
    pass


def escape_quotes(text: str) -> str:
    return re.sub(r'(?<!\\)"', '\\"', text)


def support_unicode():
    """Check whether operating system supports main symbols or not."""
    encoding = getattr(sys.stdout, "encoding")
    if encoding is None:
        encoding = locale.getpreferredencoding(False)

    try:
        encoding = codecs.lookup(encoding).name
    except Exception:
        encoding = "utf-8"
    return encoding == "utf-8"


class Span(t.NamedTuple):
    start: int
    end: int


class Entry:
    def __init__(self, span: Span, msgid: str, msgstr: str) -> None:
        self.span = span
        self.msgid = msgid
        self.msgstr = msgstr

    @staticmethod
    def _format_text(title: str, text: str, width: int) -> t.List[str]:
        text = escape_quotes(text)
        if pangu is not None:
            text = pangu.spacing_text(text)
        if len(title) + len(text) + 3 <= width:
            # 1 space + 2 quotes = 3
            return [f'{title} "{text}"']
        return [f'{title} ""'] + [
            f'"{line}"'
            for line in textwrap.wrap(text, width - 2, drop_whitespace=False)
        ]

    def format(self, width: int) -> t.List[str]:
        return self._format_text("msgid", self.msgid, width) + self._format_text(
            "msgstr", self.msgstr, width
        )


class Source:
    def __init__(
        self, filename: str, lines: t.Optional[t.Sequence[str]] = None
    ) -> None:
        self.filename = filename
        if lines is None:
            lines = [line for line in Path(filename).read_text("utf-8").splitlines()]
        self.lines = lines
        self._original = self.lines[:]
        self.lineno = -1
        self._entries: t.List[Entry] = []

    def __iter__(self) -> t.Iterator[str]:
        return self

    def __next__(self) -> str:
        self.lineno += 1
        if self.lineno >= len(self.lines):
            raise StopIteration()
        return self.lines[self.lineno]

    def parse_error(self, message: str, lineno: t.Optional[int] = None) -> str:
        if lineno is None:
            lineno = self.lineno
        raise ParseError(f"line {lineno}: {message}")

    def parse(self) -> None:
        if self.lineno >= 0:
            raise RuntimeError("Can't parse multiple times on one source")
        for line in self:
            if line.startswith("#, ") and line[3:].strip() == "fuzzy":
                # Don't modify the fuzzy entries
                self._parse_entry()
            if not line.strip() or line.startswith("#"):
                continue
            elif line.startswith("msgid"):
                self.lineno -= 1
                self._entries.append(self._parse_entry())
            else:
                self.parse_error("Unexpected token")

    def _parse_entry(self) -> Entry:
        msgid, msgstr = [], []
        temp = []
        start_line = self.lineno

        for line in self:
            if not line.strip() or line.startswith("#"):
                break
            if line.startswith("msgid"):
                if msgid:
                    self.lineno -= 1
                    break
                match = re.match(MESSAGE_RE, line[6:])
                if not match:
                    self.parse_error('Expect `msgid "..."`')
                msgid.append(match.group(1))
                start_line = self.lineno
                temp = msgid
            elif line.startswith("msgstr"):
                if msgstr:
                    self.lineno -= 1
                    break
                match = re.match(MESSAGE_RE, line[7:])
                if not match:
                    self.parse_error('Expect `msgstr: "..."`')
                msgstr.append(match.group(1))
                temp = msgstr
            else:
                match = re.match(MESSAGE_RE, line)
                if not match:
                    self.parse_error('Expect `"..."`')
                temp.append(match.group(1))

        if not msgstr:
            self.parse_error("Missing msgstr")
        return Entry(Span(start_line, self.lineno), "".join(msgid), "".join(msgstr))

    def fix(self, line_length: int, show: bool = False) -> bool:
        self.parse()
        for entry in reversed(self._entries):
            self.lines[entry.span.start : entry.span.end] = entry.format(line_length)
        return self.diff(show)

    def diff(self, show: bool = False) -> bool:
        has_diff = False
        show_title = False
        for line in difflib.unified_diff(
            self._original, self.lines, "Original", "Current", lineterm=""
        ):
            if show:
                if not show_title:
                    print(f"Need update: {self.filename}")
                    show_title = True
                print(line)
            has_diff = True
        return has_diff

    def write(self, path: t.Union[str, Path]) -> None:
        Path(path).write_text("\n".join(self.lines) + "\n", encoding="utf-8")


def cli(argv: t.Optional[t.Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Format PO files for consistency")
    parser.add_argument(
        "--line-length", type=int, default=76, help="The max length of msgid and msgstr"
    )
    parser.add_argument(
        "-c", "--check", action="store_true", help="Check only, don't modify files"
    )
    parser.add_argument(
        "filename",
        nargs="*",
        default=[os.getcwd()],
        help="Filenames to format, default to all po files under "
        "the current directory(recursively)",
    )
    args = parser.parse_args(argv)

    identical, changed, errors = 0, 0, 0
    if support_unicode():
        ERROR, SUCCESS = "❌", "✨"
    else:
        ERROR, SUCCESS = ":(", ":)"

    for filename in args.filename:
        if os.path.isdir(filename):
            filename = os.path.join(filename, "**/*.po")
        for path in glob.glob(filename, recursive=True):
            source = Source(path)
            try:
                if source.fix(args.line_length, args.check):
                    if not args.check:
                        source.write(path)
                        print(f"{SUCCESS} {path} is updated")
                    changed += 1
                else:
                    identical += 1
            except ParseError as e:
                errors += 1
                print(f"{ERROR} {path} Parse error: {e}")
                continue

    print(
        f"\nChecked {identical + changed + errors} file(s), "
        f"{errors} error file(s) and {changed} file(s) changed."
    )
    if changed or errors:
        return 1
    return 0
