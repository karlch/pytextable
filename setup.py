# vim: ft=python fileencoding=utf-8 sw=4 et sts=4

import ast
import os
import re
import setuptools


try:
    BASEDIR = os.path.dirname(os.path.realpath(__file__))
except NameError:
    BASEDIR = None


def read_file(filename):
    """Read content of filename into string and return it."""
    with open(filename) as f:
        return f.read()


def read_from_init(name):
    """Read value of a __magic__ value from the __init__.py file."""
    field_re = re.compile(r"__{}__\s+=\s+(.*)".format(re.escape(name)))
    path = os.path.join(BASEDIR, "pytextable", "__init__.py")
    line = field_re.search(read_file(path)).group(1)
    return ast.literal_eval(line)


setuptools.setup(
    python_requires=">=3.6",
    install_requires=[],
    packages=setuptools.find_packages(),
    name="pytextable",
    version=".".join(str(num) for num in read_from_init("version_info")),
    description=read_from_init("description"),
    long_description=read_file(os.path.join(BASEDIR, "README.rst")),
    author=read_from_init("author"),
    author_email=read_from_init("email"),
    url=read_from_init("url"),
    license=read_from_init("license"),
    keywords=["latex", "tables", "data"],
    zip_safe=True,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU General Public License v3 or later " "(GPLv3+)",
        "Natural Language :: English",
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Text Processing",
        "Topic :: Text Processing :: Markup :: LaTeX",
    ],
)
