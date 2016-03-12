import subprocess
import shlex

from basepipe import BasePipe

class ProcessPipe(BasePipe):
    """A pipe with local process.

    :param cmd: command to execute.
    :type cmd: str
    :param kwargs: :class:`.BasePipe` options.
    """
    def __init__(self, cmd, **kwargs):
        popen = subprocess.Popen(shlex.split(cmd), stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=False)
        super(ProcessPipe, self).__init__(popen.stdin, popen.stdout, **kwargs)
        self.popen = popen

def popen(*args, **kwargs):
    """Alias of :class:`.ProcessPipe`.
    """
    return ProcessPipe(*args, **kwargs)
