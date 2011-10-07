# -*- coding: utf-8 -*-

"""
Package configuraiton information for Importastic.
"""

import os
import sys

from setuptools import setup
from setuptools import find_packages


# requires
requires = {}

def get_long_desc():
    """
    Concat README.rst and CHANGES.txt into one string.
    """

    here = os.path.abspath(os.path.dirname(__file__))
    readme_file = open(os.path.join(here, 'README'))
    README = readme_file.read()
    changes_file = open(os.path.join(here, 'CHANGES.rst'))
    CHANGES = changes_file.read()

    return README + '\n\n' +  CHANGES

def main():
    """
    Script entry point.
    """
    setup(name = 'importastic',
          version = '0.1',
          description = """
Python import system to allow pluggable packages to be imported as
packages. Example: foo_bar to be imported as foo.bar
""",
          long_description = get_long_desc(),
          classifiers=[
              "Programming Language :: Python",
              "Development Status :: 3 - Alpha",
              "Intended Audience :: Developers",
              "License :: OSI Approved :: BSD License",
              "Topic :: Utilities"
              ],
          keywords = 'import system pluggable',
          author = 'michr',
          author_email = 'example@example.com',
          url = 'https://github.com/michr/importastic',
          license='BSD',
          packages=find_packages(exclude = ['ez_setup', 'examples', 'tests']),
          include_package_data = True,
          zip_safe = False,
          install_requires = requires,
          entry_points = "",
          )

if __name__ == '__main__':
    main()

