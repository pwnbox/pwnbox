# pwnbox

## Installation

In your python environment:

	pip install git+https://github.com/protos37/pwnbox

## Usage

### Piped communication

```python
import pwnbox

# Open pipes
pipe = pwnbox.SocketPipe("example.com", 80)

# Send request
pipe.write("GET / HTTP/1.0\r\nHost: example.com\r\n\r\n")

# Receive response header
pipe.read(until = "\r\n\r\n")

# Receive reponse body
pipe.read()
```
