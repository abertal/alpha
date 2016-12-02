============
Installation
============

.. contents::
   :depth: 3

.. Stable version
.. ==============

.. Use pip to get latest stable version, just type as usual `pip install django-mtr-sync` or add to your `requirements.txt` file. By default it will use `openpyxl` for `xlsx` format. You can change this by changing `PROCESSORS` and `default_processor`.

Development version
===================

Use one pip command to install package::

   pip install git+https://github.com/mtrgroup/django-mtr-sync.git#egg=django-mtr-sync --process-dependency-links

You can get it the latest source from our `git`_ repository::

   git clone git://github.com/mtrgroup/django-mtr-sync.git django-mtr-sync

Add the resulting folder to your `PYTHONPATH`_ or symlink the ``mtr`` directory
inside it into a directory which is on your PYTHONPATH, such as your Python
installation's ``site-packages`` directory.

You can verify that the application is available on your PYTHONPATH by
opening a Python interpreter and entering the following commands::

   >>> import mtr.sync
   >>> mtr.sync.VERSION
   (0, 1)

When you want to update your copy of the source code, run ``git pull``
from within the ``django-mtr-sync`` directory.

.. caution::

   The development version may contain bugs which are not present in the
   release version and introduce backwards-incompatible changes.

   If you're tracking master, keep an eye on the recent `Commit History`_
   before you update your copy of the source code.

.. _`git`: http://git-scm.com/
.. _`PYTHONPATH`: http://docs.python.org/tut/node8.html#SECTION008110000000000000000
.. _`Commit History`: http://github.com/mtrgroup/django-mtr-sync/commits/master
