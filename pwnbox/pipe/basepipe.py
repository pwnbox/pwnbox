import os
import sys
import string
import select
from functools import wraps

STDIN = object()
STDOUT = object()
STDERR = object()

def not_closed(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self._closed:
            raise ValueError("operation to closed pipe")
        return func(self, *args, **kwargs)
    return wrapper

def fdopen(fd, mode, buffering=0):
    if not isinstance(fd, int):
        fd = fd.fileno()
    return os.dup(fd)

def printable(data):
    return "".join(["\\x%02x" % ord(i) if i not in string.printable else i for i in data])

class BasePipe(object):
    """BasePipe(log_to=stderr, logging=True)

    Base class of pipes.

    :param log_to: (optional) fd to write logs. Set ``None`` to disable logging.
    :param logging: (optional) use ``log_to`` instead.
    :type logging: bool
    """
    def __init__(self, file_in, file_out, log_to=STDERR, logging=True):
        self._file_in = fdopen(file_in, 'wb')
        self._file_out = fdopen(file_out, 'rb')
        self._buffer_in = ""
        self._buffer_out = ""
        if log_to == STDERR:
            self._log_to = sys.stderr
        elif not logging:
            self._log_to = None
        else:
            self._log_to = log_to
        self._closed = False

    def _log_read(self, data):
        if self._log_to:
            self._log_to.write("\033[01;32m" + printable(data) + "\033[0m")

    def _log_write(self, data):
        if self._log_to:
            self._log_to.write("\033[01;34m" + printable(data) + "\033[0m")

    def _read(self):
        rfds = []
        while not self._file_out in rfds:
            rfds, _, _ = select.select([self._file_out], [], [])
        self._buffer_out += os.read(self._file_out, 4096)

    def _write(self):
        wfds = []
        while not self._file_in in wfds:
            _, wfds, _ = select.select([], [self._file_in], [])
        size = os.write(self._file_in, self._buffer_in)
        self._buffer_in = self._buffer_in[size:]

    def _flush(self):
        while self._buffer_in:
            self._write()

    def _close(self):
        os.close(self._file_in)
        os.close(self._file_out)
        self._closed = True

    @not_closed
    def read(self, size=4096):
        """Read up to ``size`` bytes of data from pipe. Function blocks until at least a byte of data is available.

        :param size: (optional) maximum size of data in bytes to read.
        :type size: int
        :return: data read from pipe.
        """
        while not self._buffer_out:
            self._read()
        data, self._buffer_out = self._buffer_out[:size], self._buffer_out[size:]
        self._log_read(data)
        return data

    @not_closed
    def read_until(self, until):
        """Read until ``until`` appears in pipe. Function blocks until ``until`` appears in available data.

        :param until: string to read until.
        :type until: str
        :return: data read from pipe ends with ``until``.
        """
        logged = 0
        while not until in self._buffer_out:
            self._log_read(self._buffer_out[logged:])
            logged = len(self._buffer_out)
            self._read()
        data, until, self._buffer_out = self._buffer_out.partition(until)
        data += until
        self._log_read(data[logged:])
        return data

    @not_closed
    def read_some(self):
        """Read up some data from pipe. Function blocks until at least a byte of data is available.

        :return: data read from pipe.
        """
        return self.read()

    @not_closed
    def read_byte(self, count = 1):
        """Read exactly ``count`` bytes of data from pipe. Function blocks until ``count`` bytes of data is available.

        :param byte: (optional) size of data in bytes to read.
        :type byte: int
        :return: data read from pipe.
        """
        logged = 0
        while len(self._buffer_out) < count:
            self._log_read(self._buffer_out[:logged])
            logged = len(self._buffer_out)
            self._read()
        data, self._buffer_out = self._buffer_out[:count], self._buffer_out[count:]
        self._log_read(data[logged:])
        return data

    @not_closed
    def read_line(self, line = 1):
        """Read exactly ``line`` lines of data from pipe. Function blocks until ``line`` ``\\n`` appears in available data.

        :param line: (optional) lines to read.
        :type line: int
        :return: data read from pipe including ``\\n``.
        """
        data = ""
        for i in xrange(line):
            data += self.read_until("\n")
        return data

    @not_closed
    def write(self, data):
        """Write ``buf`` to pipe.

        :param buf: data to be written.
        :type buf: str
        """
        self._buffer_in += data
        self._flush()
        self._log_write(data)

    @not_closed
    def write_line(self, data):
        """Write ``data`` with ``\\n`` to pipe.

        :param data: data to be written.
        :type data: str
        """
        self.write(data + "\n")

    @not_closed
    def interact(self, stdin=STDIN, stdout=STDOUT):
        """interact(stdin=stdin, stdout=stdout)

        Interact pipe directly with standard IO. Graceful return is not guaranteed.

        :param stdin: (optional) standard input fd.
        :param stdout: (optional) standard output fd.
        """
        stdin = fdopen(sys.stdin if stdin is STDIN else stdin, "rb")
        stdout = fdopen(sys.stdout if stdout is STDOUT else stdout, "wb")

        while not self._closed:
            rfds = [stdin, self._file_out]
            wfds = []
            if self._buffer_in:
                wfds.append(self._file_in)
            if self._buffer_out:
                wfds.append(stdout)
            rfds, wfds, _ = select.select(rfds, wfds, [])
            if stdin in rfds:
                data = os.read(stdin, 4096)
                if data == "":
                    break
                self._buffer_in += data
            if self._file_out in rfds:
                data = os.read(self._file_out, 4096)
                if data == "":
                    break
                self._buffer_out += data
            if stdout in wfds:
                size = os.write(stdout, self._buffer_out)
                self._buffer_out = self._buffer_out[size:]
            if self._file_in in wfds:
                size = os.write(self._file_in, self._buffer_in)
                self._buffer_in = self._buffer_in[size:]

        while self._buffer_out:
            _, wfds, _ = select.select([], [stdout], [])
            if stdout in wfds:
                size = os.write(stdout, self._buffer_out)
                self._buffer_out = self._buffer_out[size:]

        os.close(stdin)
        os.close(stdout)

    def close(self):
        """Close pipe.
        """
        self._close()
