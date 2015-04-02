# pwnbox

[![Build Status](https://travis-ci.org/protos37/pwnbox.svg?branch=master)](https://travis-ci.org/protos37/pwnbox)

## Installation

In your python environment:

	pip install git+https://github.com/protos37/pwnbox

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

### Number Theory

```python
import pwnbox

print pwnbox.number.power(2, 20, 1000)
# 576

print pwnbox.number.MillerRabin(179428398)
# False

print pwnbox.number.MillerRabin(179428399)
# True

for i in pwnbox.number.prange(100000, 100100):
	print i,
# 100003 100019 100043 100049 100057 100069
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
```
