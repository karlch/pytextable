Contributing Guidelines
=======================

You want to contribute to pytextable? Great! Every little help counts and is appreciated!

Need help? Feel free to `contact me directly <karlch@protonmail.com>`_
or open an
`issue on github <https://github.com/karlch/pytextable/issues/>`_.

.. contents::

Feedback and Feature Requests
-----------------------------

Any feedback is welcome! Did you find something unintuitive? Not clearly documented? Do
you have a great idea for a new feature? Let me know!  You can either open an
`issue directly on github <https://github.com/karlch/pytextable/issues/>`_
or `contact me directly <karlch@protonmail.com>`_ if you prefer.

You like pytextable? Share some love and spread the word!

Reporting Bugs
--------------

The best way to report bugs is to open an `issue on github
<https://github.com/karlch/pytextable/issues/>`_. If you do not have a github account,
feel free to `contact me directly <karlch@protonmail.com>`_. If possible, please
include the traceback of the exception and instructions on how to reproduce the bug.

Writing Code
------------

You probably already know what you want to work on as you are reading this
page. If you want to implement a new feature, it might be a good idea to open a
feature request on the `issue tracker
<https://github.com/karlch/pytextable/issues/>`_ first. Otherwise you might be
disappointed if I do not accept your pull request because I do not feel like
this should be in the scope of pytextable.

If you want to find something to do, check the
`issue tracker`_.

If you like, you can also find some more information on
`the api <https://pytextable.readthedocs.io/en/latest/api.html>`_.

Writing Documentation
---------------------

More documentation is always useful! Here are some options where this could be done:

* Improving the website. Is something unclear or missing?
* Extending and improve the docstrings in the code base.
* Writing blog posts, articles, ... All of them are appreciated! If you like, they can
  also be linked here.

In case you choose to update the website, here are some more tips.
The website is written in
`resturctured Text (reST) <https://en.wikipedia.org/wiki/ReStructuredText>`_
and built using
`sphinx <http://www.sphinx-doc.org/en/master/>`_.
A great introduction is given by the
`reST Primer of sphinx <http://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html>`_.

You can find the reST files used to build the website in the project's ``docs`` folder.
If you would like to build a local copy, you can run::

    tox -e docs -- path/to/copy

You can then browse your local build::

    $BROWSER path/to/copy/index.html
