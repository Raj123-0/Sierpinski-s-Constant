import importlib.util
import os
import tempfile

import pytest


@pytest.fixture(scope="module")
def module():
    spec = importlib.util.spec_from_file_location(
        "sierpinski_module", "MODULE_FILENAME"
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# Known value of Sierpinski's constant (OEIS A240882):
#   2.584981759579253...
# Digit string (decimal point removed) begins with "2584981759..."
KNOWN_PREFIX = "2584981759"


def test_known_prefix(module):
    digits = module.compute_sierpinski(50)
    assert digits.startswith(KNOWN_PREFIX)
    assert len(digits) == 50


def test_digit_string_no_decimal(module):
    digits = module.compute_sierpinski(30)
    assert "." not in digits
    assert all(c in "0123456789" for c in digits)


def test_leading_digit_is_two(module):
    """Sierpinski's constant is ~2.585, so the first digit must be '2'."""
    digits = module.compute_sierpinski(20)
    assert digits[0] == "2"


def test_output_files_created(module, tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    module.compute_sierpinski(40)

    raw_path = tmp_path / "Sierpinski_40_digits.txt"
    b_path = tmp_path / "b_file_Sierpinski_40.txt"

    assert raw_path.exists()
    assert b_path.exists()

    raw_content = raw_path.read_text(encoding="utf-8")
    assert raw_content.startswith(KNOWN_PREFIX)
    assert len(raw_content) == 40

    b_lines = b_path.read_text(encoding="utf-8").strip().split("\n")
    assert len(b_lines) == 40
    # First b-file line: index 1, first digit '2'
    assert b_lines[0] == "1 2"
    # Fifth line: index 5, fifth digit (0-indexed 4) of "25849..." = '9'
    assert b_lines[4] == "5 9"
    # Verify every line has format "<idx> <digit>"
    for i, line in enumerate(b_lines, start=1):
        parts = line.split()
        assert len(parts) == 2
        assert int(parts[0]) == i
        assert parts[1] in "0123456789"


def test_consistency_across_sizes(module):
    small = module.compute_sierpinski(20)
    large = module.compute_sierpinski(100)
    assert large.startswith(small)


def test_cli_default_digits(module, tmp_path, monkeypatch):
    """Running with -n 10 produces a 10-digit raw file."""
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr("sys.argv", ["prog", "-n", "10"])
    module.main()
    raw = tmp_path / "Sierpinski_10_digits.txt"
    assert raw.exists()
    content = raw.read_text(encoding="utf-8")
    assert len(content) == 10
    assert content.startswith(KNOWN_PREFIX)
