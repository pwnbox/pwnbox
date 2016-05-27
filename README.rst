======
pwnbox
======

.. image:: https://travis-ci.org/pwnbox/pwnbox.svg?branch=master
    :target: https://travis-ci.org/pwnbox/pwnbox

.. image:: https://readthedocs.org/projects/pwnbox/badge/?version=latest
    :target: http://pwnbox.readthedocs.org/en/latest/?badge=latest

Python toolbox for hacking and problem solving

Installation
============

In order to use `pwnbox.number`, gmpy2 should be installed.

.. code-block:: bash

  brew install libmpc
  pip install gmpy2

In your python environment:

.. code-block:: bash

	pip install git+https://github.com/pwnbox/pwnbox

To upgrade:

.. code-block:: bash

	pip install --upgrade pwnbox

Examples
========

General purpose pipe interface:

.. code-block:: python

    import pwnbox

    # Open pipes
    # pipe = pwnbox.pipe.popen("nc example.com 80")
    pipe = pwnbox.pipe.connect("example.com", 80)

    # Send request
    pipe.write("GET / HTTP/1.0\r\nHost: example.com\r\n\r\n")

    # Receive response header
    pipe.read_until("\r\n\r\n")

    # Interact with standard IO
    pipe.interact()

    # Close pipe
    pipe.close()

Number theory implementations:

- Chinese Remainder Theorem
- Weiner's attack
- Fermat's factorization
- Pollard's rho method


Utilties:

.. code-block:: python

    from pwnbox.utils import *

    # DWORD to Little Endian
    l = dtol(1234)

    # QWORD to Big Endian
    b = qtob(1234)

    # Little Endian to Integer
    i = ltoi("\x01\x02\x03\x04")

    # string operations
    a = sand(dtol(0x12345678), dtol(0xffff0000))
    x = sxor(dtol(0xdeafbeef), dtol(0x12345678))

Documentation
=============

Documents are available at `http://pwnbox.readthedocs.org/`.
