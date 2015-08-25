import unittest
import imp
import pwnbox

class TestImport(unittest.TestCase):
    def test_has_gmpy2(self):
        has_gmpy2 = False
        try:
            imp.find_module('gmpy2')
            has_gmpy2 = True
        except ImportError:
            pass
        if has_gmpy2:
            try:
                pwnbox.number
            except AttributeError:
                self.fail('pwnbox.number not imported with gmpy2')
        else:
            with self.assertRaises(AttributeError):
                pwnbox.number
