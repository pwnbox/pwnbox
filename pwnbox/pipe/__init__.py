"""General purpose pipe interface.

.. autoclass:: BasePipe
   :members:

.. autofunction:: pipe

.. autoclass:: Pipe
   :members:

.. autofunction:: connect

.. autoclass:: SocketPipe
   :members:

.. autofunction:: popen

.. autoclass:: ProcessPipe
   :members:

"""

from .basepipe import BasePipe
from .socketpipe import SocketPipe, connect
from .processpipe import ProcessPipe, popen
from .pipe import Pipe, pipe
