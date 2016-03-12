======
pwnbox
======

.. image:: https://travis-ci.org/protos37/pwnbox.svg?branch=master
    :target: https://travis-ci.org/protos37/pwnbox

.. image:: https://readthedocs.org/projects/pwnbox/badge/?version=latest
    :target: http://pwnbox.readthedocs.org/en/latest/?badge=latest

Python toolbox for hacking and problem solving

Installation
============

In your python environment:

.. code-block:: bash

	pip install git+https://github.com/protos37/pwnbox

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

    import pwnbox

    # DWORD to Little Endian
    l = pwnbox.utils.dtol(1234)

    # QWORD to Big Endian
    b = pwnbox.utils.qtob(1234)

    # Little Endian to Integer
    i = pwnbox.utils.ltoi("\x01\x02\x03\x04")

    # string operations
    a = pwnbox.utils.sand(pwnbox.utils.dtol(0x12345678), pwnbox.utils.dtol(0xffff0000))
    x = pwnbox.utils.sxor(pwnbox.utils.dtol(0xdeafbeef), pwnbox.utils.dtol(0x12345678))

Documentation
=============

Documentation is available at `http://pwnbox.readthedocs.org/`.
