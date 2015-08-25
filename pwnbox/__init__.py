import imp

import pipe
import utils

has_gmpy2 = False
try:
    imp.find_module('gmpy2')
    has_gmpy2 = True
except ImportError:
    pass

if has_gmpy2:
    import number
