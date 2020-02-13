Usage
=====

Installation
------------

Using pip
^^^^^^^^^

.. code::

    pip install [--user] pytextable

Manual installation
^^^^^^^^^^^^^^^^^^^

First, you have to get the source code::

    git clone https://github.com/karlch/pytextable

Then, switch to the repository::

    cd pytextable

And run::

    python setup.py install [--user]

Grabbing the source file
^^^^^^^^^^^^^^^^^^^^^^^^

The ``_pytextable.py`` source file is self-contained. You can copy it,put it anywhere
you like and just use it from there.


Examples
--------

As examples speak louder than words, let's look at some python code and the latex
output it produces. First, you will need to import the module and have some data you
would like to write to a latex table::

    import pytextable

    # This is usually your 2d numpy array or any sequence of sequences
    DATA = [[1.2346, 1, 1.2346], [1.2346, 1.2346, 1.2346], [1.2346, 1.2346, 1.2346]]

Default table
^^^^^^^^^^^^^

Let's start with the defaults::

    >>> pytextable.tostring(DATA)
    \begin{table}
        \centering
        \begin{tabular}{ccc}
            \toprule
            1.2346 & 1 & 1.2346 \\
            1.2346 & 1.2346 & 1.2346 \\
            1.2346 & 1.2346 & 1.2346 \\
            \bottomrule
        \end{tabular}
    \end{table}

If you would like to write the table to a file instead, you can call write directly::

    >>> pytextable.write(DATA)

Write supports all the options ``tostring`` does, so we will continue the examples just
using ``tostring``.

Formatting
^^^^^^^^^^

You may not like the number of digits used for the formatting and that the ``1`` has no
digits at all. To fix this, you can pass the ``fmt`` argument::

    >>> pytextable.tostring(DATA, fmt=".3f")
    \begin{table}
        \centering
        \begin{tabular}{ccc}
            \toprule
            1.235 & 1.000 & 1.235 \\
            1.235 & 1.235 & 1.235 \\
            1.235 & 1.235 & 1.235 \\
            \bottomrule
        \end{tabular}
    \end{table}

The formatting is applied to every single element. If you have a more complicated use
case, please pre-format each row as a sequence of strings in the format you like.

Header
^^^^^^

Next, let's add a header to our table::

    >>> pytextable.tostring(DATA, fmt=".3f", header=("first", "second", "third"))
    \begin{table}
        \centering
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

Caption and label
^^^^^^^^^^^^^^^^^

Pretty neat, but as good citizens we would like to add a caption and a lable to our
table::

    >>> pytextable.tostring(
        DATA,
        fmt=".3f",
        header=("first", "second", "third"),
        caption="My fancy pytextable",
        label="tab:pytextable",
    )
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

Table alignment
^^^^^^^^^^^^^^^

By default all elements of the table are center-aligned and no seperators are added. You
can change this, by passing another alignment, for example::

    >>> pytextable.tostring(DATA, alignment="l")
    \begin{table}
        \centering
        \begin{tabular}{lll}
            \toprule
            1.2346 & 1 & 1.2346 \\
            1.2346 & 1.2346 & 1.2346 \\
            1.2346 & 1.2346 & 1.2346 \\
            \bottomrule
        \end{tabular}
    \end{table}


This concludes the basic usage of ``pytextable``. For a list of all the options, please
refer to the :doc:`the api documentation <api>`.
