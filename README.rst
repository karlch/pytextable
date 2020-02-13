pytextable - create latex tables using pure python
==================================================

.. warning::

    pytextable is not yet available on PyPI but v0.1.0 should be out very soon,
    stay tuned!

.. image:: https://github.com/karlch/pytextable/workflows/CI/badge.svg
   :target: https://github.com/karlch/pytextable/actions
   :alt: CI
.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/ambv/black
   :alt: Code style: black

**pytextable** creates well-formatted latex tables with booktabs support in pure python.

**pytextable** is highly-configurable, you decide how your table should look.

**pytextable** is small, fast and requires nothing but ``python>=3.6``.


Quick Start Guide
-----------------

#. Install

   .. code:: console

        pip install pytextable

#. Import

   .. code:: python

        import pytextable

#. Create a latex table from your data :)


   .. code:: python

        pytextable.write(data, "table.tex")


Example
-------

.. code:: python

    import pytextable

    # This is usually your 2d numpy array or any sequence of sequences
    DATA = [[1.2346, 1, 1.2346], [1.2346, 1.2346, 1.2346], [1.2346, 1.2346, 1.2346]]

    >>> pytextable.tostring(
        DATA,
        fmt=".3f",
        header=("first", "second", "third"),
        caption="My fancy pytextable",
        label="tab:pytextable",
    )
    r"""
    \begin{table}
        \centering
        \caption{My fancy pytextable}
        \label{tab:pytextable}
        \begin{tabular}{ccc}
            \toprule
            first & second & third \\
            \midrule
            1.235 & 1.000 & 1.235 \\
            1.235 & 1.235 & 1.235 \\
            1.235 & 1.235 & 1.235 \\
            \bottomrule
        \end{tabular}
    \end{table}
    """

    # To write to file use pytextable.write(DATA, filename)
    >>> pytextable.write(DATA, "table.tex", fmt=".3f", ...)


Links
-----

* `Read the full documentation here <https://pytextable.readthedocs.io/en/latest>`_.


License
-------

This program is free software: you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free Software
Foundation, either version 3 of the License, or (at your option) any later
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with
this program. If not, see <http://www.gnu.org/licenses/>.
