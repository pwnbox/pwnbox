# pwnbox

[![Build Status](https://travis-ci.org/protos37/pwnbox.svg?branch=master)](https://travis-ci.org/protos37/pwnbox)

## Installation

In your python environment:

	pip install git+https://github.com/protos37/pwnbox

To upgrade:

	pip install --upgrade pwnbox

## Usage

### Piped communication

```python
import pwnbox

# Open pipes
# pipe = pwnbox.pipe.ProcessPipe("nc example.com 80")
# pipe = pwnbox.pipe.StringPipe("HTTP/1.0 200 OK\r\n\r\nIt Works!")
pipe = pwnbox.pipe.SocketPipe("example.com", 80)

# Send request
pipe.write("GET / HTTP/1.0\r\nHost: example.com\r\n\r\n")

# Receive response header
pipe.read_until("\r\n\r\n")

# Receive reponse body
pipe.read()

# Close pipe
pipe.close()
```

### Utilities

```python
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
```
