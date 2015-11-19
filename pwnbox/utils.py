"""Miscellaneous utilties.
"""

import operator

def dtol(num):
    """Integer to DWORD in little endian.
    """
    return ("%08x" % (num & 0xFFFFFFFF)).decode("hex")[::-1]

def dtob(num):
    """Integer to DWORD in big endian.
    """
    return ("%08x" % (num & 0xFFFFFFFF)).decode("hex")

def qtol(num):
    """Integer to QWORD in little endian.
    """
    return ("%016x" % (num & 0xFFFFFFFFFFFFFFFF)).decode("hex")[::-1]

def qtob(num):
    """Integer to QWORD in big endian.
    """
    return ("%016x" % (num & 0xFFFFFFFFFFFFFFFF)).decode("hex")

def ltoi(mem):
    """Little endian bytes to integer.
    """
    return int(mem[::-1].encode("hex"), 16)

def btoi(mem):
    """Big endian bytes to integer.
    """
    return int(mem.encode("hex"), 16)

def sopr(a, b, f):
    t = max(len(a), len(b))
    return "".join([chr(f(ord(a.ljust(t, "\x00")[i]), ord(b.ljust(t, "\x00")[i]))) for i in xrange(t)])

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
    return "".join([chr(ord(i) ^ 0xff) for i in a])
