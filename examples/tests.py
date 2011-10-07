#!/usr/bin/env python

# test import of a real method from a fake module
from pharaoh.foo.bar import method_in_a_fake_module
# test import of a real method from a REAL module inside a fake module
from pharaoh.foo.bat import method_in_a_real_module

