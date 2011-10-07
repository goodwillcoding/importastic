Importastic
###########

Python import hook for pluggable architecture. Largely Based on Flask's
extension import hook but enhanced to support real nested modules.

Currently in development, only been tested on Linux.

What it does
============

Lets say you have projects named ``foo`` and ``foo_bar``.
Adding following code to foo/__init__.py will let you import ``foo_bar`` as ``foo.bar"``

::
    
    def setup():
        from importastic.exthook import ExtensionImporter
        importer = ExtensionImporter(['foo_%s'], __name__)
        importer.install()
    
    setup()
    del setup


The separator (i.e "_") is customizable.


Trying It Out
=============

1. Create a virtualenv
2. run ``./install_examples``
3. ``cd examples``
4. ``python ./tests.py``


Disclaimer
==========

Use at your own risk. It might kill kittens.


License
=======

BSD.