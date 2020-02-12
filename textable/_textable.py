# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

"""Utilities to convert python data to latex tables."""

import typing


DataT = typing.List[typing.List[typing.Any]]


def tostring(
    data: DataT,
    *,
    header: typing.List[str] = None,
    table: bool = True,
    centering: bool = True,
    caption: str = "",
    label: str = "",
    alignment: str = "",
    fmt: str = "",
    numspace: int = 4,
    booktabs: bool = True,
    midrule_condition=lambda _row, _last_row: False,
) -> str:
    n_columns = _get_num_columns(data)
    _check_to_string(data)
    content = _create_table_rows(
        data,
        header=header,
        fmt=fmt,
        booktabs=booktabs,
        midrule_condition=midrule_condition,
    )
    content = _wrap_tex_environment(
        "tabular", content, cmd=_table_alignment(alignment, n_columns)
    )
    if table:
        if label:
            content = f"\\label{{{label}}}\n{content}"
        if caption:
            content = f"\\caption{{{caption}}}\n{content}"
        if centering:
            content = f"\\centering\n{content}"
        content = _wrap_tex_environment("table", content)
    return content


def write(data: DataT, outfile: str, *, writemode: str = "w", **kwargs) -> None:
    with open(outfile, writemode) as f:
        f.write(tostring(data, **kwargs))


def _get_num_columns(data: DataT) -> int:
    n_columns = sorted({len(row) for row in data})
    if len(n_columns) != 1:
        found = ", ".join(str(num) for num in n_columns)
        raise ValueError(
            f"All rows must have the same number of columns. Found: {found}."
        )
    return n_columns[0]


def _check_to_string(data: DataT):
    for row in data:
        for elem in row:
            str(elem)


def _create_table_rows(
    data: DataT,
    *,
    header: typing.List[str] = None,
    fmt: str = "",
    booktabs: bool = True,
    midrule_condition=lambda row: False,
) -> str:
    ROW_END = r" \\"

    def create_row(row: typing.List[typing.Any], fmt=fmt):
        text = " & ".join(f"{elem:{fmt}}" for elem in row)
        return text + ROW_END

    headstr = create_row(header, fmt="") if header is not None else ""
    rows = []
    last_elem = data[0]
    for elem in data:
        row = create_row(elem)
        if midrule_condition(elem, last_elem):
            row += "\n\\midrule"
        rows.append(row)
        last_elem = elem
    rowstr = "\n".join(rows)
    if booktabs and headstr:
        return f"\\toprule\n{headstr}\n\\midrule\n{rowstr}\n\\bottomrule"
    if booktabs:
        return f"\\toprule\n{rowstr}\n\\bottomrule"
    if headstr:
        return f"{headstr} \\hline\n{rowstr}"
    return rowstr


def _wrap_tex_environment(
    environment: str,
    text: str,
    *,
    cmd: str = "",
    options: str = "",
    indentation: int = 4,
) -> str:
    options = f"[{options}]" if options else ""
    cmd = f"{{{cmd}}}" if cmd else ""
    begin = rf"\begin{{{environment}}}{cmd}{options}"
    inner_lines = [
        " " * indentation + line for line in text.split("\n") if line.strip()
    ]
    content = "\n".join(inner_lines)
    end = rf"\end{{{environment}}}"
    return f"{begin}\n{content}\n{end}\n"


def _table_alignment(alignment: str, n_columns: int):
    if not alignment:
        return "c" * n_columns

    align_chars = "lcr|"
    if set(alignment) - set(align_chars):
        raise ValueError(
            f"Invalid alignment '{alignment}'. Must only contain: {align_chars}."
        )
    alignment_chars = alignment.replace("|", "")
    n_alignment_chars = len(alignment_chars)

    if n_alignment_chars == n_columns:
        return alignment
    if n_alignment_chars == 1:
        raw_alignment = alignment_chars * n_columns
        if len(alignment) == 1:
            return raw_alignment
        elif len(alignment) == 2:
            return "|".join(raw_alignment)
        elif len(alignment) == 3:
            return "|" + "|".join(raw_alignment) + "|"
        raise ValueError(
            f"Too many | separators passed to alignment '{alignment}'. "
            "Must pass exactly 1 or 2."
        )

    raise ValueError(
        f"Number of alignment characters ({n_alignment_chars}) "
        "must match number of columns {n_columns}."
    )
