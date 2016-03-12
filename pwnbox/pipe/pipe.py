import os

from basepipe import BasePipe

class Pipe(BasePipe):
    """An echo pipe with ``os.pipe()``.

    :param kwargs: :class:`.BasePipe` options.
    """
    def __init__(self, **kwargs):
        self.rfd, self.wfd = os.pipe()
        super(Pipe, self).__init__(self.wfd, self.rfd, **kwargs)

    def close(self):
        super(Pipe, self).close()
        os.close(self.rfd)
        os.close(self.wfd)

def pipe(*args, **kwargs):
    """Alias of :class:`.Pipe`.
    """
    return Pipe(*args, **kwargs)
