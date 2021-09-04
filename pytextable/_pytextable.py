# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

"""Utilities to convert python data to latex tables."""

import functools
import typing


RowT = typing.Sequence[typing.Any]
DataT = typing.Sequence[RowT]
HeaderT = typing.Sequence[str]
MidruleCallbackT = typing.Callable[[RowT, RowT], bool]


def _no_extra_midrule(_row: RowT, _last_row: RowT) -> bool:
    """Default callback that does not add any extra midrules to the table."""
    return False


def tostring(
    data: DataT,
    *,
    header: HeaderT = None,
    table: bool = True,
    centering: bool = True,
    caption: str = "",
    label: str = "",
    alignment: str = "",
    fmt: str = "",
    indentation: int = 4,
    booktabs: bool = True,
    midrule_condition: MidruleCallbackT = _no_extra_midrule,
) -> str:
    r"""Convert python data to a valid tex table string.

    This is the heart of pytextable and does all the heavy lifting. You must pass the
    data argument which containts the rows and columns of the table to create. The other
    keyword-only arguments allow additional formatting and customization.

    Args:
        data: Sequence of sequences containing the rows and columns of the table. Note
            that the number of columns in each row must match.
        header: Column header to add as sequence of strings. The number of elements must
            match the number of columns of your data.
        table: Add a surrounding table environment to the latex tabular.
        centering: Add a \centering statement to the table. This is only valid if
            ``table=True``.
        caption: Add this caption to the table. This is only valid if ``table=True``.
        label: Add this label to the table. This is only valid if ``table=True``.
        alignment: String converted to the full table alignment. Examples:

            >>> _table_alignment("", 3)  # The default
            "ccc"

            >>> _table_alignment("l", 3)  # Left-align everything instead
            "lll"

            >>> _table_alignment("l|", 3)  # Left-align and add separators in the table
            "l|l|l"

            >>> _table_alignment("|l|", 3)  # Left-align and add separators everywhere
            "|l|l|l|"

            >>> _table_alignment("llc", 3)  # Valid-formatter is just accepted
            "llc"

            >>> _table_alignment("|ll|l|", 3)  # Separators are fine as-well
            "|ll|l|"

        fmt: Format string to apply to every element in the table data. Example: '.3f'.
        indentation: Number of spaces used for environment indentation.
        booktabs: Use the booktabs module to neatly format the table.
        midrule_condition: Callback to check for additional inserted midrules. This
            function is called with the current and previous row and should return a
            boolean. If it returns True, a ``\midrule`` is applied before the current
            row. Example:

            >>> def second_elem_changed(row, last_row):
                return row[1] != last_row[1]

            This is useful to separate the current row from the previous one in case
            something changed. Only valid with ``booktabs=True``.

    Returns:
        The latex table as formatted string.
    """
    n_columns = _get_num_columns(data)
    content = _create_table_rows(
        data,
        header=header,
        fmt=fmt,
        booktabs=booktabs,
        midrule_condition=midrule_condition,
    )
    wrap = functools.partial(_wrap_tex_environment, indentation=indentation)
    content = wrap("tabular", content, cmd=_table_alignment(alignment, n_columns))
    if table:
        if label:
            content = f"\\label{{{label}}}\n{content}"
        if caption:
            content = f"\\caption{{{caption}}}\n{content}"
        if centering:
            content = f"\\centering\n{content}"
        content = wrap("table", content)
    return content


def write(
    data: DataT,
    outfile: str,
    *,
    writemode: str = "w",
    encoding: str = "utf-8",
    **kwargs: typing.Any,
) -> None:
    r"""Write python data to file as formatted latex table.

    Calls :func:`tostring` to convert the data to a valid tex table passing any
    additional keyword-arguments on. The retrieved string is then written to the file
    passed.

    Args:
        data: Sequence of sequences containing the rows and columns of the table. Note
            that the number of columns in each row must match.
        outfile: File to write the data to.
        writemode: Writemode to use when opening the file. Note that the mode must
            support writing, passing ``r`` will fail horribly for obvious reasons. This
            argument exists to give the option to append to a file with ``a``.
        encoding: Encoding to use when opening the file. The default of ``utf-8`` works
            well with latex code using ``\usepackage[utf8]{inputenc}``.
        kwargs: Keyword arguments for additional formatting passed to :func:`tostring`.
    """
    with open(outfile, writemode, encoding=encoding) as f:
        f.write(tostring(data, **kwargs))


def _get_num_columns(data: DataT) -> int:
    """Return the number of columns in every row.

    If the number of columns is not equal for every row, a ValueError is raised.
    """
    n_columns = sorted({len(row) for row in data})
    if len(n_columns) != 1:
        found = ", ".join(str(num) for num in n_columns)
        raise ValueError(
            f"All rows must have the same number of columns. Found: {found}."
        )
    return n_columns[0]


def _create_table_rows(
    data: DataT,
    *,
    header: HeaderT = None,
    fmt: str = "",
    booktabs: bool = True,
    midrule_condition: MidruleCallbackT = _no_extra_midrule,
) -> str:
    """Create string of latex table rows from python data.

    Args:
        data: List of lists containing the rows and columns of the table.
        header: Header of every column as valid string if any.
        fmt: Format string to apply to every element in the row. Example: '.3g'.
        booktabs: Use the booktabs module to neatly format the table.
        midrule_condition: Callback to check for additional inserted midrules.
    """
    row_end = r" \\"

    def create_row(row: RowT, fmt: str = fmt) -> str:
        text = " & ".join(f"{elem:{fmt}}" for elem in row)
        return text + row_end

    headstr = create_row(header, fmt="") if header is not None else ""
    rows = []
    last_elem = data[0]
    for elem in data:
        row = create_row(elem)
        if midrule_condition(elem, last_elem):
            row = "\n\\midrule\n" + row
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
    r"""Wrap text in a tex environment.

    Examples:
        >>> _wrap_tex_environment("center", "My custom text")
        \begin{center}
            My custom text
        \end{center}

        >>> _wrap_tex_environment("tabular", "1 & 2 \\", cmd="ll")
        \begin{tabular}{ll}
            1 & 2 \\
        \end{tabular}

    Args:
        environment: The tex environment to wrap the text in.
        text: Text to wrap in an environment.
        cmd: Additional command to pass to the environment as {cmd}.
        options: Additional options to pass to the environment as [options].
        indentation: Number of spaces used for indenting the text.
    """
    options = f"[{options}]" if options else ""
    cmd = f"{{{cmd}}}" if cmd else ""
    begin = rf"\begin{{{environment}}}{cmd}{options}"

    inner_lines = [
        " " * indentation + line for line in text.split("\n") if line.strip()
    ]
    content = "\n".join(inner_lines)

    end = rf"\end{{{environment}}}"

    return f"{begin}\n{content}\n{end}\n"


def _table_alignment(alignment: str, n_columns: int) -> str:
    """Return a valid latex tabular alignment string.

    See :func:`write` vor valid examples.

    Args:
        alignment: Simplified string converted to the full table alignment.
        n_columns: Number of columns for which the alignment is created.
    """
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
        if len(alignment) == 2:
            return "|".join(raw_alignment)
        if len(alignment) == 3:
            return "|" + "|".join(raw_alignment) + "|"
        raise ValueError(
            f"Too many | separators passed to alignment '{alignment}'. "
            "Must pass exactly 1 or 2."
        )

    raise ValueError(
        f"Number of alignment characters ({n_alignment_chars}) "
        "must match number of columns {n_columns}."
    )
