Importastic
###########

Python import hook for pluggable architecture. Largely Based on Flask's
extension import hook but enhanced to support real nested modules.

Currently in development, only been tested on Linux.

What it does (the docs)
=======================

Lets say you have projects named ``foo`` and ``foo_bar``.
Adding following code to foo/__init__.py will let you import ``foo_bar`` as 
``foo.bar"``

::
    
    def setup():
        from importastic.exthook import ExtensionImporter
        importer = ExtensionImporter(['foo_%s'], __name__)
        importer.install()
    
    setup()
    del setup


The separator (i.e "_") is customizable.


Why would anyone use it
=======================

The author used it re-organize a large code base without running too many sed
statements. Flask project uses something similar to backwardly import plugins.


Trying It Out
=============


1. Create a virtualenv and activate it
2. git clone https://github.com/michr/importastic.git
3. run ``./install_examples``
4. ``cd examples``
5. ``python ./tests.py``


Disclaimer
==========

Use at your own risk. It might kill kittens.


License
=======

BSD.
