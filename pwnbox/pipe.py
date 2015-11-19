"""General purpose pipe interface.
"""

import sys
import os
import socket
import subprocess
import shlex
import fcntl
import telnetlib
import os
import select
import string

class Pipe(object):
    """Base class of Pipe Objects.
    """
    def __init__(self, logging = True):
        self.readbuf = ""
        self.writebuf = ""
        self.logging = logging
        self.stderr = sys.stderr

    def readlog(self, buf):
        if self.logging:
            buf = "".join(["\\x%02x" % ord(i) if i not in string.printable else i for i in buf])
            self.stderr.write("\033[01;32m" + buf + "\033[0m")

    def writelog(self, buf):
        if self.logging:
            buf = "".join(["\\x%02x" % ord(i) if i not in string.printable else i for i in buf])
            self.stderr.write("\033[01;34m" + buf + "\033[0m")

    def read(self, size = 4096):
        """Read up to ``size`` bytes of data from pipe. Function blocks until at least a byte of data is available.

        :param size: (optional) maximum size of data in bytes to read.
        :type size: int
        :return: data read from pipe.
        """
        if not self.readbuf:
            self._read()
        buf, self.readbuf = self.readbuf[:size], self.readbuf[size:]
        self.readlog(buf)
        return buf

    def read_until(self, until):
        """Read until ``until`` appears in pipe. Function blocks until ``until`` appears in available data.

        :param until: string to read until.
        :type until: str
        :return: data read from pipe including ``until``.
        """
        log = 0
        while not until in self.readbuf:
            self.readlog(self.readbuf[log:])
            log = len(self.readbuf)
            self._read()
        buf, tok, self.readbuf = self.readbuf.partition(until)
        buf += tok
        self.readlog(buf[log:])
        return buf

    def read_some(self):
        """Read up some data from pipe. Function blocks until at least a byte of data is available.

        :return: data read from pipe.
        """
        return self.read()

    def read_byte(self, byte = 1):
        """Read exactly ``byte`` bytes of data from pipe. Function blocks until ``byte`` bytes of data is available.

        :param byte: (optional) size of data in bytes to read.
        :type byte: int
        :return: data read from pipe.
        """
        log = 0
        while len(self.readbuf) < byte:
            self.readlog(self.readbuf[log:])
            log = len(self.readbuf)
            self._read()
        buf = self.readbuf[:byte]
        self.readbuf = self.readbuf[byte:]
        self.readlog(buf[log:])
        return buf

    def read_line(self, line = 1):
        """Read exactly ``line`` lines of data from pipe. Function blocks until ``line`` ``\\n`` appears in available data.

        :param line: (optional) lines to read.
        :type line: int
        :return: data read from pipe including ``\\n``.
        """
        buf = ""
        for i in range(line):
            buf += self.read_until("\n")
        return buf

    def write(self, buf):
        """Write ``buf`` to pipe.

        :param buf: data to be written.
        :type buf: str
        """
        self.writebuf += buf
        self._write()
        self.writelog(buf)
 
    def write_line(self, buf):
        """Write ``buf`` with ``\\n`` to pipe.

        :param buf: data to be written.
        :type buf: str
        """
        self.write(buf + "\n")

    def interact(self):
        """Interact pipe directly with standard IO.
        """
        sys.stdout.write(self.readbuf)
        self.readbuf = ""
        self._interact()

    def close(self):
        """Close pipe.
        """
        self._close()

class StringPipe(Pipe):
    """A pipe from string data. Useful when simulating pipe.

    :param data: data to be pushed into read buffer.
    :type data: str
    :param logging: (optional) set ``False`` to disable logging.
    :type logging: bool
    """
    def __init__(self, data, **kwargs):
        if "logging" in kwargs:
            super(StringPipe, self).__init__(kwargs["logging"])
        else:
            super(StringPipe, self).__init__()
        self.readbuf = data

    def _read(self):
        pass

    def _write(self):
        self.writebuf = ""

    def _close(self):
        pass

class SocketPipe(Pipe):
    """A pipe with TCP server.

    :param addr: network address of remote server.
    :type addr: str
    :param port: port number of remote server.
    :type port: int
    :param logging: (optional) set ``False`` to disable logging.
    :type logging: bool
    """
    def __init__(self, addr = None, port = None, **kwargs):
        if "logging" in kwargs:
            super(SocketPipe, self).__init__(kwargs["logging"])
        else:
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
    """A pipe with local process.

    :param cmd: command to execute.
    :type cmd: str
    """
    def __init__(self, cmd = None, **kwargs):
        if "logging" in kwargs:
            super(ProcessPipe, self).__init__(kwargs["logging"])
        else:
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
