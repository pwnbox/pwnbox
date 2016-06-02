import unittest
import os
import threading
import socket

from pwnbox import pipe

data = (b"Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.\n"
        b"Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.\n"
        b"Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.\n"
        b"Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.\n")

class PipeTest(object):
    def test_read_write(self):
        self.pipe.write(data)
        read = self.pipe.read()
        self.assertNotEqual(len(read), 0)
        self.assertEqual(read, data[:len(read)])

    def test_read_byte(self):
        self.pipe.write(data)
        read = self.pipe.read_byte(100)
        self.assertEqual(read, data[:100])
        read += self.pipe.read_byte(len(data) - 100)
        self.assertEqual(read, data)

    def test_read_line(self):
        self.pipe.write(data)
        for line in data.split(b"\n")[:-1]:
            self.assertEqual(self.pipe.read_line(), line + b"\n")

    def test_read_until(self):
        self.pipe.write(data)
        read = b""
        for until in [b"Lorem", b"ipsum", b".\n", b"non proident", b"laborum.\n"]:
            now = self.pipe.read_until(until)
            self.assertNotIn(until, now[:-1])
            self.assertIn(until, now)
            read += now
            self.assertEqual(read, data[:len(read)])

    def test_interact(self):
        def interact():
            self.pipe.interact(r.rfd, w.wfd)
        r, w = pipe.Pipe(log_to=None), pipe.Pipe(log_to=None)
        thread = threading.Thread(target=interact)
        thread.setDaemon(True)
        thread.start()
        for i in range(3):
            r.write(data)
            read = w.read_byte(len(data))
            self.assertEqual(read, data)
        r.close(), w.close()

    def tearDown(self):
        self.pipe.close()

class TestPipe(PipeTest, unittest.TestCase):
    def setUp(self):
        self.pipe = pipe.Pipe(log_to=None)

class TestProcessPipe(PipeTest, unittest.TestCase):
    def setUp(self):
        self.pipe = pipe.ProcessPipe("cat", log_to=None)

class TestSocketPipe(PipeTest, unittest.TestCase):
    def setUp(self):
        def server():
            conn, _ = self.sock.accept()
            while True:
                data = conn.recv(4096)
                if data == b"":
                    break
                conn.sendall(data)
            conn.close()
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("", 0))
        self.sock.listen(1)
        thread = threading.Thread(target=server)
        thread.setDaemon(True)
        thread.start()
        _, port = self.sock.getsockname()
        self.pipe = pipe.SocketPipe("localhost", port, log_to=None)

    def tearDown(self):
        self.pipe.close()
        self.sock.close()
