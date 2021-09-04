Changelog
=========

All notable changes to pytextable are documented in this file.


v0.3.0 (unreleased)
-------------------


v0.2.1 (2021-09-04)
-------------------

Bugfix release due to erroneous tag pushed for v0.2.0.


v0.2.0 (2021-09-04)
-------------------

Changed:
^^^^^^^^

* Additional midrules from ``midrule_condition`` are now prepended to the current row
  instead of appended. This makes more sense as we can check if the current row is
  different from the previous one. If so, we want to separate the current row from the
  previous row, not the current row from the next one.
* New ``encoding`` keyword argument for the ``write`` function. The default of ``utf-8``
  is sane and works well with latex code using ``\usepackage[utf8]{inputenc}``.



v0.1.0 (2020-02-13)
-------------------

Initial release of pytextable.
