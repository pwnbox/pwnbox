# pwnbox

## Installation

In your python environment:

	pip install git+https://github.com/protos37/pwnbox

## Usage

### Piped communication

```python
import pwnbox

# Open pipes
# pipe = pwnbox.ProcessPipe("nc example.com 80")
pipe = pwnbox.SocketPipe("example.com", 80)

# Send request
pipe.write("GET / HTTP/1.0\r\nHost: example.com\r\n\r\n")

# Receive response header
pipe.read(until = "\r\n\r\n")

# Receive reponse body
pipe.read()
```

### Utilities

```python
import pwnbox

# DWORD to Little Endian
l = pwnbox.dtol(1234)

# QWORD to Big Endian
b = pwnbox.qtob(1234)

# Little Endian to Integer
i = pwnbox.ltoi("\x01\x02\x03\x04")
```
