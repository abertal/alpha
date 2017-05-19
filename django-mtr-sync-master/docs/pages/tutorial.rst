========
Tutorial
========


The Problem
===========

You've created a Django project, and you need to manage data in it.


The Solution
============

Sync let you forgot about writing repeated code for simple and rootine export and import data in different formats. Of course you have full customization of the process and you can extend app as you want using simple `register` callbacks.


Getting started
===============


Add ``mtr.sync`` To ``INSTALLED_APPS``
--------------------------------------

As with most Django applications, you should add ``mtr.sync`` to the ``INSTALLED_APPS`` in your ``settings.py`` file::

    INSTALLED_APPS = (
        'django.contrib.auth',
        # ...
        'mtr.sync',
    )


Set up additional dependencies for different formats
----------------------------------------------------

Now migrate app

    python manage.py migrate mtr_sync

Note: as you can see we use low dash to split submodule, this convetion is for urls and database tables, so for example, your own app `sync` will not conflict at least for django 1.7+

Start import or export your data
----------------------

Start a server and go to admin section 'http://localhost:8000/admin/mtr_sync/'

Subclass admin mixins for shortcut urls
---------------------------------------

Use class `SyncAdminMixin` for admin shortcut links and `SyncTabularInlineMixin` with `SyncStackedInlineMixin` for tabular and stacked inlines respectively. 