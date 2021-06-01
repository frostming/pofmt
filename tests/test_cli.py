import shutil
from pathlib import Path

from pofmt.core import cli

FIXTURES = Path(__file__).parent / "fixtures"


def test_find_po_files(tmp_path, capfd):
    golden = FIXTURES / "golden.po"
    dest_paths = [tmp_path / "a.po", tmp_path / "deep/inner/path/b.po"]
    for path in dest_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FIXTURES / "raw.po", path)

    result = cli([str(tmp_path)])
    assert result != 0
    out, _ = capfd.readouterr()
    assert "Checked 2 file(s)" in out
    assert "2 file(s) changed" in out
    for path in dest_paths:
        assert path.read_text("utf-8") == golden.read_text("utf-8")


def test_passing_glob_pattern(tmp_path, capfd):
    golden = FIXTURES / "golden.po"
    raw = FIXTURES / "raw.po"
    dest_paths = [tmp_path / "a.po", tmp_path / "deep/inner/path/b.po"]
    for path in dest_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FIXTURES / "raw.po", path)

    result = cli([f"{tmp_path}/*.po"])
    assert result != 0
    out, _ = capfd.readouterr()
    assert "Checked 1 file(s)" in out
    assert "1 file(s) changed" in out

    assert dest_paths[0].read_text("utf-8") == golden.read_text("utf-8")
    assert dest_paths[1].read_text("utf-8") == raw.read_text("utf-8")


def test_check_without_update(tmp_path, capfd):
    raw = FIXTURES / "raw.po"
    dest_paths = [tmp_path / "a.po", tmp_path / "deep/inner/path/b.po"]
    for path in dest_paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(FIXTURES / "raw.po", path)

    result = cli(["--check", str(tmp_path)])
    assert result != 0
    out, _ = capfd.readouterr()
    assert "Need update" in out
    assert "Checked 2 file(s)" in out
    assert "2 file(s) changed" in out

    for path in dest_paths:
        assert path.read_text("utf-8") == raw.read_text("utf-8")
