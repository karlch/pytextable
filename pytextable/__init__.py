# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

"""Utilities to convert python data to latex tables."""

__license__ = "GPL3"
__version_info__ = (0, 1, 0)
__version__ = ".".join(str(num) for num in __version_info__)
__author__ = "Christian Karl"
__maintainer__ = __author__
__email__ = "karlch@protonmail.com"
__description__ = "Utilities to convert python data to latex tables."
__url__ = "https://github.com/karlch/pytextable"


from ._pytextable import tostring, write, DataT, RowT, HeaderT, MidruleCallbackT
