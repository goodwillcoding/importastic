# -*- coding: utf-8 -*-

"""
    Taken from Flask Project:

    https://github.com/mitsuhiko/flask/blob/master/flask/exthook.py
    https://github.com/mitsuhiko/flask/blob/master/flask/ext/__init__.py

    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

def setup():
    from importastic.exthook import ExtensionImporter
    importer = ExtensionImporter(['pharaoh_foo_%s'], __name__)
    importer.install()

setup()
del setup
