========
Overview
========

.. contents::
   :depth: 3

What is ``django-mtr-sync``?
========================

``django-mtr-sync`` is a reusable Django app which let's you easy export and import data using django admin interfac so you don't need to write similar code.

Feature overview
----------------

* Import and export data
* Processor API for supporting other formats
* Uses Celery for background tasks and for processing large volumes of data
* Creates reports about importing and exporting operations
* Auto discovering models for use in package
* Data range settings (start, end cells in table), for example, if you need to import data where there is a header with logo or any other unnecessary information
* Field settings:
  * maps model fields with data fields
  * adds and removes fields (ability to skip fields on import)
  * set start cell of exporting data
  * related models import-export by choosing main model
* Supports: CSV(native python3, unicodecsv python2), XLS (using: xlwt-future, xlrd), XLSX (using: openpyxl optimized writer, reader mode, for fast processing of large volumes of data) and ODS(odfpy)
* Saves import, export settings for the processing of data from various sources and for simplicity
* Integration with standart django admin app
* Custom filters (for querysets)
* Modeltransation language activation
* Inline support
* Value processors (convert values before import or export)
* Shortcuts at admin app
* Multilingual (i18n)
* Template integration with django-grapelli
* Action handler for more flexebility (for example not create model but generate source code for it, prepare data for model)
* Supports: Django 1.6-1.8+ Python 2.7, 3.3+
