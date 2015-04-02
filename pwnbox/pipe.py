import sys
import os
import socket
import subprocess
import shlex
import fcntl
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
        if not self.readbuf:
            self._read()
        buf, self.readbuf = self.readbuf, ""
        self.readlog(buf)
        return buf

    def read_until(self, until):
        log = 0
        while not until in self.readbuf:
            self.readlog(self.readbuf[log:])
            log = len(self.readbuf)
            self._read()
        buf, tok, self.readbuf = self.readbuf.partition(until)
        buf += tok
        self.readlog(buf[log:])
        return buf

    def read_bytes(self, byte=1):
        log = 0
        while len(self.readbuf) < byte:
            self.readlog(self.readbuf[log:])
            log = len(self.readbuf)
            self._read()
        buf = self.readbuf[:byte]
        self.readbuf = self.readbuf[byte:]
        self.readlog(buf[log:])
        return buf

    def read_line(self, lines = 1):
        buf = ""
        for i in range(lines):
            buf += self.read_until("\n")
        return buf

    def write(self, buf):
        self.writebuf += buf
        self._write()
        self.writelog(buf)
 
    def write_line(self, buf):
        self.write(buf + "\n")

    def interact(self):
        sys.stdout.write(self.readbuf)
        self.readbuf = ""
        self._interact()

    def close(self):
        self._close()

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

    def _interact(self):
        tn = telnetlib.Telnet()
        tn.sock = self.sock
        tn.interact()

    def _close(self):
        self.sock.close()

class ProcessPipe(Pipe):
    def __init__(self, cmd = None, **kwargs):
        super(ProcessPipe, self).__init__()
        if "popen" in kwargs:
            self.popen = kwargs["popen"]
        else:
            self.popen = subprocess.Popen(shlex.split(cmd), stdin = subprocess.PIPE, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell = False)
        fcntl.fcntl(self.popen.stdout, fcntl.F_SETFL, fcntl.fcntl(self.popen.stdout, fcntl.F_GETFL) | os.O_NONBLOCK)

    def _read(self):
        try:
            self.readbuf += self.popen.stdout.read()
        except IOError as e:
            if e.strerror.lower() != "Resource temporarily unavailable".lower():
                raise e

    def _write(self):
        self.popen.stdin.write(self.writebuf)
        self.popen.stdin.flush()
        self.writebuf = ""

    def _interact(self):
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
                while data != "":
                    n = os.write(termout, data)
                    data = data[n:]
            if termin in r:
                data = os.read(termin, 4096)
                if data == "":
                    break
                while data != "":
                    n = os.write(childin, data)
                    data = data[n:]

    def _close(self):
        self.popen.terminate()
