import sys
import socket
import subprocess
import shlex
import telnetlib
import os
import select

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
        elif "bytes" in kwargs:
            log = 0
            while len(self.readbuf) < int(kwargs["bytes"]):
                self.readlog(self.readbuf[log:])
                log = len(self.readbuf)
                self._read()
            buf = self.readbuf[:int(kwargs["bytes"])]
            self.readbuf = self.readbuf[int(kwargs["bytes"]):]
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

    def close(self):
        self._close()

    def readline(self, lines = 1):
        buf = ""
        for i in range(lines):
            buf += self.read(until = "\n")
        return buf

    def writeline(self, buf):
        self.write(buf + "\n")

class StringPipe(Pipe):
    def __init__(self, data):
        super(StringPipe, self).__init__()
        self.readbuf = data

    def _read(self):
        pass

    def _write(self):
        self.writebuf = ""

    def _close(self):
        pass

class SocketPipe(Pipe):
    def __init__(self, addr = None, port = None, **kwargs):
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

    def _close(self):
        self.sock.close()

    def interact(self):
        tn = telnetlib.Telnet()
        tn.sock = self.sock
        tn.interact()

class ProcessPipe(Pipe):
    def __init__(self, cmd = None, **kwargs):
        super(ProcessPipe, self).__init__()
        if "popen" in kwargs:
            self.popen = kwargs["popen"]
        else:
            self.popen = subprocess.Popen(shlex.split(cmd), stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT)

    def _read(self):
        self.readbuf += self.popen.stdout.readline()

    def _write(self):
        self.popen.stdin.write(self.writebuf)
        self.popen.stdin.flush()

    def _close(self):
        self.popen.terminate()

    def interact(self):
        termin = sys.stdin.fileno()
        termout = sys.stdout.fileno()
        childin = self.popen.stdin.fileno()
        childout = self.popen.stdout.fileno()

        while True:
            r, w, e = select.select([termin, childout], [], [])
            if childout in r:
                data = os.read(childout, 4096)
                if data == "":
                    break
                os.write(termout, data)
            if termin in r:
                data = os.read(termin, 4096)
                while data != "":
                    n = os.write(childin, data)
                    data = data[n:]
