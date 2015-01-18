import unittest
import pwnbox

class TestStringPipe(unittest.TestCase):
    def setUp(self):
        self.pipe = pwnbox.StringPipe("Hello World!\n")

    def test_read(self):
        s = ""
        while len(s) < len("Hello World!\n"):
            s += self.pipe.read()
        self.assertEqual("Hello World!\n", s)

    def test_readline(self):
        self.assertEqual("Hello World!\n", self.pipe.readline())

    def test_readuntil(self):
        self.assertEqual("Hello World!", self.pipe.read(until = "rld!"))
        self.assertEqual("\n", self.pipe.read(until = "\n"))

    def test_readbytes(self):
        self.assertEqual("Hello W", self.pipe.read(bytes = 7))
        self.assertEqual("orld!", self.pipe.read(bytes = 5))

    def tearDown(self):
        self.pipe.close()

class TestProcessPipe(unittest.TestCase):
    def setUp(self):
        self.pipe = pwnbox.ProcessPipe("cat")

    def test_readwrite(self):
        self.pipe.write("Hello World!\n")
        s = ""
        while len(s) < len("Hello World!\n"):
            s += self.pipe.read()
        self.assertEqual("Hello World!\n", s)

    def tearDown(self):
        self.pipe.close()
