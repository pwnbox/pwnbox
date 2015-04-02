import unittest
from pwnbox import pipe

class TestStringPipe(unittest.TestCase):
    def setUp(self):
        self.pipe = pipe.StringPipe("Hello World!\n")

    def test_read(self):
        s = ""
        while len(s) < len("Hello World!\n"):
            s += self.pipe.read()
        self.assertEqual("Hello World!\n", s)

    def test_read_line(self):
        self.assertEqual("Hello World!\n", self.pipe.read_line())

    def test_read_until(self):
        self.assertEqual("Hello World!", self.pipe.read_until("rld!"))
        self.assertEqual("\n", self.pipe.read_until("\n"))

    def test_read_bytes(self):
        self.assertEqual("Hello W", self.pipe.read_bytes(7))
        self.assertEqual("orld!", self.pipe.read_bytes(5))

    def tearDown(self):
        self.pipe.close()

class TestProcessPipe(TestStringPipe):
    def setUp(self):
        self.pipe = pipe.ProcessPipe("echo \"Hello World!\"")
