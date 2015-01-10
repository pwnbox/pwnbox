import sys
import socket

class Pipe(object):
    def __init__(self):
        self.readbuf = ""
        self.writebuf = ""
        self.log = sys.stderr

    def readlog(self, buf):
        self.log.write("\033[01;32m" + buf + "\033[0m")

    def writelog(self, buf):
        self.log.write("\033[01;34m" + buf + "\033[0m")

    def read(self, **kwargs):
        if "until" in kwargs:
            log = 0
            while not kwargs["until"] in self.readbuf:
                self.readlog(self.readbuf[log:])
                log = len(self.readbuf)
                self._read()
            buf, tok, self.readbuf = self.readbuf.partition(kwargs["until"])
            buf += tok
            self.readlog(buf[log:])
        else:
            if not self.readbuf:
                self._read()
            buf, self.readbuf = self.readbuf, ""
            self.readlog(buf)
        return buf

    def write(self, buf):
        self.writebuf += buf
        self._write()
        self.writelog(buf)

    def readline(self, lines = 1):
        buf = ""
        for i in range(lines):
            buf += self.read(until = "\n")
        return buf
    
    def writeline(self, buf):
        self.write(buf + "\n")

class SocketPipe(Pipe):
    def __init__(self, addr, port, **kwargs):
        super(SocketPipe, self).__init__()

        if "socket" in kwargs:
            self.sock = kwargs["socket"]
        else:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((addr, port))

    def _read(self):
        self.readbuf += self.sock.recv(4096)

    def _write(self):
        while self.writebuf:
            wrt = self.sock.send(self.writebuf)
            self.writebuf = self.writebuf[wrt:]
