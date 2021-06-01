import textwrap
from pathlib import Path

import pytest

from pofmt.core import ParseError, Source

FIXTURES = Path(__file__).parent / "fixtures"


@pytest.mark.parametrize("n", range(10))
def test_format_file_consistent(n):
    """Run several times to see if the content is consistent"""
    golden = FIXTURES / "golden.po"
    raw = FIXTURES / "raw.po"
    s = Source(raw)
    assert s.fix(76)
    content = "\n".join(s.lines) + "\n"
    assert content == golden.read_text(encoding="utf-8")


@pytest.mark.parametrize(
    "error_text",
    [
        textwrap.dedent(
            """msgid
    msgstr "hello"
    """
        ),
        textwrap.dedent(
            """msgid "hello
    msgstr "world"
    """
        ),
        'msgstr "hello world"',
        textwrap.dedent(
            """msgid ""
        hello world"
        msgstr "foobar"
        """
        ),
    ],
)
def test_parse_error(error_text):
    s = Source("test_file", error_text.splitlines())
    with pytest.raises(ParseError):
        s.parse()
