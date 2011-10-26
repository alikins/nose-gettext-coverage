import sys
# try:
#     import ez_setup
#     ez_setup.use_setuptools()
# except ImportError:
#     pass

from setuptools import setup

setup(
    name='gettext-coverage',
    version='0.2',
    author='Adrian Likins',
    author_email = 'alikins@redhat.com',
    description = 'coverage of gettext strings',
    license = 'GNU LGPL',
    py_modules = ['gettext_coverage'],
    entry_points = {
        'nose.plugins.0.10': [
            'gettext_coverage = gettext_coverage:GettextCoverage'
            ]
        }

    )
