import socket

from basepipe import BasePipe

class SocketPipe(BasePipe):
    """A pipe with a TCP connection.

    :param addr: network address of remote server.
    :type addr: str
    :param port: port number of remote server.
    :type port: int
    :param kwargs: :class:`.BasePipe` options.
    """
    def __init__(self, addr, port, **kwargs):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((addr, port))
        super(SocketPipe, self).__init__(sock, sock, **kwargs)
        self.sock = sock

    def close(self):
        super(SocketPipe, self).close()
        self.sock.close()

def connect(*args, **kwargs):
    """Alias of :class:`.SocketPipe`.
    """
    return SocketPipe(*args, **kwargs)
