from setuptools import setup, find_packages

import os


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

README = read('README.md')

version = '0.1'  # hardcoded, because of circular namespace dependencies

setup(
    name='django-mtr-sync',
    packages=find_packages(exclude=('tests/', 'docs/')),
    version=version,
    author='mtr group',
    author_email='inboxmtr@gmail.com',
    url='https://github.com/mtrgroup/django-mtr-sync',
    description=README,
    long_description=README,
    namespace_packages=('mtr',),
    zip_safe=False,
    include_package_data=True,
    classifiers=(
        'Framework :: Django',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ),
    keywords=(
        'django', 'xlsx', 'import data', 'export data', 'csv', 'ods', 'xls'),
    dependency_links=[
        'https://github.com/mtrgroup/django-mtr-utils/tarball/master'
        '#egg=django-mtr-utils-0.1',
    ],
    install_requires=[
        'django>=1.7', 'django-mtr-utils==0.1', 'xlrd', 'ezodf', 'lxml',
        'openpyxl<=2.1', 'xlwt-future', 'unicodecsv'
    ],
)
