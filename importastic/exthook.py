# -*- coding: utf-8 -*-

"""
    Redirect imports for extensions.  This module basically makes it possible
    for us to transition from phraoh.foo to pharaoh_foo without having to
    force all extensions to upgrade at the same time.

    Lets say you have a project called `pharaoh`

    When a user does ``from pharaoh.ext.foo import bar`` it will attempt to
    import ``from pharaoh_foo import bar``.

    Orignal code from Flask Project:

    https://github.com/mitsuhiko/flask/blob/master/flask/exthook.py
    https://github.com/mitsuhiko/flask/blob/master/flask/ext/__init__.py

    :copyright: (c) 2011 by Armin Ronacher.
    :license: BSD, see LICENSE for more details.
"""

import imp
import os
import sys


class ExtensionImporter(object):
    """This importer redirects imports from this submodule to other locations.
    This makes it possible to transition from the old flaskext.name to the
    newer flask_name without people having a hard time.
    """

    def __init__(self, module_choices, wrapper_module):
        self.module_choices = module_choices
        self.wrapper_module = wrapper_module
        self.prefix = wrapper_module + '.'
        self.prefix_cutoff = wrapper_module.count('.') + 1

    def __eq__(self, other):
        return self.__class__.__module__ == other.__class__.__module__ and \
               self.__class__.__name__ == other.__class__.__name__ and \
               self.wrapper_module == other.wrapper_module and \
               self.module_choices == other.module_choices

    def __ne__(self, other):
        return not self.__eq__(other)

    def install(self):
        sys.meta_path[:] = [x for x in sys.meta_path if self != x] + [self]

    def find_module(self, fullname, path=None):
        if fullname.startswith(self.prefix):
            return self

    def load_module(self, fullname):
        if fullname in sys.modules:
            return sys.modules[fullname]

        # #####################################################
        # check if this is a real module but trying to find it
        # if modules is found load it
        # #####################################################
        parent_name, modname = fullname.rsplit('.', self.prefix_cutoff)
        # first see if the parent is imported
        if parent_name in sys.modules:
            # grab parent module path
            parent_path = sys.modules[parent_name].__path__
            # now try to find it
            # this should probalbly be done if find_module on top!!
            try:
                found_info = imp.find_module(modname, parent_path)
            except ImportError:
                # if not found, then we its not a real module
                pass
            else:
                # if found the module then try to load it and return it
                try:
                    module = imp.load_module(fullname, *found_info)
                    # for n in sys.modules:
                    #     if n.startswith('pharaoh_foo.') \
                    #        or n.startswith('pharaoh.foo.'):
                    #         print "    ", n, ":", sys.modules[n]
                    return module
                except ImportError:
                    exc_type, exc_value, tb = sys.exc_info()
                    sys.modules.pop(fullname, None)
                    raise exc_type, exc_value, tb

        modname = fullname.split('.', self.prefix_cutoff)[self.prefix_cutoff]
        for path in self.module_choices:
            realname = path % modname
            try:
                __import__(realname)
            except ImportError:
                exc_type, exc_value, tb = sys.exc_info()
                # since we only establish the entry in sys.modules at the
                # very this seems to be redundant, but if recursive imports
                # happen we will call into the move import a second time.
                # On the second invocation we still don't have an entry for
                # fullname in sys.modules, but we will end up with the same
                # fake module name and that import will succeed since this
                # one already has a temporary entry in the modules dict.
                # Since this one "succeeded" temporarily that second
                # invocation now will have created a fullname entry in
                # sys.modules which we have to kill.
                sys.modules.pop(fullname, None)

                # If it's an important traceback we reraise it, otherwise
                # we swallow it and try the next choice.  The skipped frame
                # is the one from __import__ above which we don't care about
                if self.is_important_traceback(realname, tb):
                    raise exc_type, exc_value, tb.tb_next
                continue
            module = sys.modules[fullname] = sys.modules[realname]
            if '.' not in modname:
                setattr(sys.modules[self.wrapper_module], modname, module)
            return module

        raise ImportError('No module named %s' % fullname)


    def is_important_traceback(self, important_module, tb):
        """Walks a traceback's frames and checks if any of the frames
        originated in the given important module.  If that is the case then we
        were able to import the module itself but apparently something went
        wrong when the module was imported.  (Eg: import of an import failed).
        """
        while tb is not None:
            if self.is_important_frame(important_module, tb):
                return True
            tb = tb.tb_next
        return False

    def is_important_frame(self, important_module, tb):
        """Checks a single frame if it's important."""
        g = tb.tb_frame.f_globals
        if '__name__' not in g:
            return False

        module_name = g['__name__']

        # Python 2.7 Behavior.  Modules are cleaned up late so the
        # name shows up properly here.  Success!
        if module_name == important_module:
            return True

        # Some python verisons will will clean up modules so early that the
        # module name at that point is no longer set.  Try guessing from
        # the filename then.
        filename = os.path.abspath(tb.tb_frame.f_code.co_filename)
        test_string = os.path.sep + important_module.replace('.', os.path.sep)
        return test_string + '.py' in filename or \
               test_string + os.path.sep + '__init__.py' in filename

