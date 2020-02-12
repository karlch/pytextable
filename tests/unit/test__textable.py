# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

"""Tests for textable._textable."""

import pytest

from textable import _textable


def test_wrap_tex_environment():
    text = "My custom text"
    expected = f"\\begin{{center}}\n    {text}\n\\end{{center}}\n"
    assert _textable._wrap_tex_environment("center", text) == expected


def test_wrap_tex_environment_cmd():
    text = "My custom text"
    cmd = "lll"
    expected = f"\\begin{{tabular}}{{{cmd}}}\n    {text}\n\\end{{tabular}}\n"
    assert _textable._wrap_tex_environment("tabular", text, cmd=cmd) == expected


def test_wrap_tex_environment_options():
    text = "My custom text"
    options = "lll"
    expected = f"\\begin{{tabular}}[{options}]\n    {text}\n\\end{{tabular}}\n"
    assert _textable._wrap_tex_environment("tabular", text, options=options) == expected


@pytest.mark.parametrize("data", [[[1, 2]], [[1, 2, 3]]])
def test_n_columns(data):
    assert len(data[0]) == _textable._get_num_columns(data)


def test_fail_columns():
    data = [
        (1, 2, 3),
        (1, 2, 3),
        (1, 2, 3),
        (1, 2, 3, 4),
    ]
    with pytest.raises(ValueError, match="All rows must have the same number"):
        _textable._get_num_columns(data)


@pytest.mark.parametrize(
    "alignment, n_columns, expected",
    (
        ("l", 3, "lll"),
        ("r", 2, "rr"),
        ("c", 4, "cccc"),
        ("l|", 3, "l|l|l"),
        ("|l|", 3, "|l|l|l|"),
        ("", 3, "ccc"),
        ("llc", 3, "llc"),
        ("|ll|l|", 3, "|ll|l|"),
    )
)
def test_table_alignment(alignment, n_columns, expected):
    assert _textable._table_alignment(alignment, n_columns) == expected


def test_fail_table_alignment_chars():
    with pytest.raises(ValueError, match="Invalid alignment"):
        _textable._table_alignment("llb", 3)


def test_fail_table_alignment_n_separators():
    with pytest.raises(ValueError, match="Too many |"):
        _textable._table_alignment("|l|||", 3)


@pytest.mark.parametrize("alignment", ("ll", "llll"))
def test_fail_table_alignment_n_chars(alignment):
    with pytest.raises(ValueError, match="Number of alignment"):
        _textable._table_alignment(alignment, 3)
