"""Miscellaneous utilties.
"""

import operator
import codecs
import six

try:
    xrange
except NameError:
    xrange = range

def dtol(num):
    """Integer to DWORD in little endian.
    """
    return codecs.decode("%08x" % (num & 0xFFFFFFFF), "hex")[::-1]

def dtob(num):
    """Integer to DWORD in big endian.
    """
    return codecs.decode("%08x" % (num & 0xFFFFFFFF), "hex")

def qtol(num):
    """Integer to QWORD in little endian.
    """
    return codecs.decode("%016x" % (num & 0xFFFFFFFFFFFFFFFF), "hex")[::-1]

def qtob(num):
    """Integer to QWORD in big endian.
    """
    return codecs.decode("%016x" % (num & 0xFFFFFFFFFFFFFFFF), "hex")

def ltoi(mem):
    """Little endian bytes to integer.
    """
    return int(codecs.encode(six.b(mem[::-1]), "hex"), 16)

def btoi(mem):
    """Big endian bytes to integer.
    """
    return int(codecs.encode(six.b(mem), "hex"), 16)

def sopr(a, b, f):
    t = max(len(a), len(b))
    return bytes(bytearray([f(ord(a.ljust(t, b"\x00")[i:i + 1]), ord(b.ljust(t, b"\x00")[i:i + 1])) for i in xrange(t)]))

def sand(a, b):
    """Bitwise and operator on string.
    """
    return sopr(a, b, operator.and_)

def sor(a, b):
    """Bitwise or operator on string.
    """
    return sopr(a, b, operator.or_)

def sxor(a, b):
    """Bitwise xor operator on string.
    """
    return sopr(a, b, operator.xor)

def sinv(a):
    """Bitwise inverse operator on string.
    """
    return bytes(bytearray([ord(a[i:i + 1]) ^ 0xff for i in xrange(len(a))]))
