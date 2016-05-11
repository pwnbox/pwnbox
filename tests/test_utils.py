import unittest
from pwnbox import utils

class TestTos(unittest.TestCase):
    def test_dtol(self):
        self.assertEqual(utils.dtol(0x01234567), b"\x67\x45\x23\x01")
        self.assertEqual(utils.dtol(0x012345ff), b"\xff\x45\x23\x01")

    def test_dtob(self):
        self.assertEqual(utils.dtob(0x01234567), b"\x01\x23\x45\x67")
        self.assertEqual(utils.dtob(0x012345ff), b"\x01\x23\x45\xff")

    def test_qtol(self):
        self.assertEqual(utils.qtol(0x0123456789abcdef), b"\xef\xcd\xab\x89\x67\x45\x23\x01")
        self.assertEqual(utils.qtol(0x0123456789abcdff), b"\xff\xcd\xab\x89\x67\x45\x23\x01")

    def test_qtob(self):
        self.assertEqual(utils.qtob(0x0123456789abcdef), b"\x01\x23\x45\x67\x89\xab\xcd\xef")
        self.assertEqual(utils.qtob(0x0123456789abcdff), b"\x01\x23\x45\x67\x89\xab\xcd\xff")

    def test_ltoi(self):
        self.assertEqual(utils.ltoi("\x67\x45\x23\x01"), 0x01234567)
        self.assertEqual(utils.ltoi("\xff\x45\x23\x01"), 0x012345ff)

    def test_btoi(self):
        self.assertEqual(utils.btoi("\x01\x23\x45\x67"), 0x01234567)
        self.assertEqual(utils.btoi("\x01\x23\x45\xff"), 0x012345ff)

class TestSoprs(unittest.TestCase):
    def test_sand(self):
        self.assertEqual(utils.sand(utils.dtol(0x12345678), utils.dtol(0xdeadbeef)), utils.dtol(0x12345678 & 0xdeadbeef))

    def test_sor(self):
        self.assertEqual(utils.sor(utils.dtol(0x12345678), utils.dtol(0xdeadbeef)), utils.dtol(0x12345678 | 0xdeadbeef))

    def test_sxor(self):
        self.assertEqual(utils.sxor(utils.dtol(0x12345678), utils.dtol(0xdeadbeef)), utils.dtol(0x12345678 ^ 0xdeadbeef))

    def test_sinv(self):
        self.assertEqual(utils.sinv(utils.dtol(0x12345678)), utils.dtol(0x12345678 ^ 0xffffffff))
