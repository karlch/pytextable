# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

"""Integration tests for textable."""

import os

import pytest

import textable


DATA = [[1.2346, 1, 1.2346], [1.2346, 1.2346, 1.2346], [1.2346, 1.2346, 1.2346]]


def midrule_for_one(rows, _last_rows):
    return 1 in rows


FILE_TO_KWARGS = {
    "default.tex": {},
    "threedigit.tex": {"fmt": ".3f"},
    "threedigit_notrailing.tex": {"fmt": ".4g"},
    "header.tex": {"header": ("first", "second", "third")},
    "notable.tex": {"table": False},
    "label.tex": {"label": "mylabel"},
    "label_caption.tex": {"label": "mylabel", "caption": "My Caption"},
    "nobooktabs.tex": {"booktabs": False},
    "nobooktabs_header.tex": {
        "booktabs": False,
        "header": ("first", "second", "third"),
    },
    "midrule_for_one.tex": {"midrule_condition": midrule_for_one},
    "nocentering.tex": {"centering": False}
}


@pytest.mark.parametrize("infile, kwargs", FILE_TO_KWARGS.items())
def test_textable(tmpdir, infile, kwargs):

    dirname = os.path.dirname(os.path.realpath(__file__))
    infile = os.path.join(dirname, "data", infile)

    def read_bytes(fname):
        with open(fname, "rb") as f:
            return f.read()

    outfile = tmpdir.join("output.tex")
    textable.write(DATA, outfile, **kwargs)
    assert read_bytes(infile) == read_bytes(outfile)
