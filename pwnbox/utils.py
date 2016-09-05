"""Miscellaneous utilties.
"""

import operator
import codecs
import six
from six.moves import zip_longest

def dtol(num):
    """Integer to DWORD in little endian.
    """
    return codecs.decode(six.b("%08x" % (num & 0xFFFFFFFF)), "hex")[::-1]

def dtob(num):
    """Integer to DWORD in big endian.
    """
    return codecs.decode(six.b("%08x" % (num & 0xFFFFFFFF)), "hex")

def qtol(num):
    """Integer to QWORD in little endian.
    """
    return codecs.decode(six.b("%016x" % (num & 0xFFFFFFFFFFFFFFFF)), "hex")[::-1]

def qtob(num):
    """Integer to QWORD in big endian.
    """
    return codecs.decode(six.b("%016x" % (num & 0xFFFFFFFFFFFFFFFF)), "hex")

def ltoi(mem):
    """Little endian bytes to integer.
    """
    return int(codecs.encode(mem[::-1], "hex"), 16)

def btoi(mem):
    """Big endian bytes to integer.
    """
    return int(codecs.encode(mem, "hex"), 16)

def sopr(a, b, f):
    return bytes(bytearray([f(*i) for i in zip_longest(six.iterbytes(a), six.iterbytes(b), fillvalue=0)]))

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
    return bytes(bytearray([i ^ 0xff for i in six.iterbytes(a)]))
