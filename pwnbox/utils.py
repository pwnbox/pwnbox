import operator

def dtol(num):
    return ("%08x" % (num & 0xFFFFFFFF)).decode("hex")[::-1]

def dtob(num):
    return ("%08x" % (num & 0xFFFFFFFF)).decode("hex")

def qtol(num):
    return ("%016x" % (num & 0xFFFFFFFFFFFFFFFF)).decode("hex")[::-1]

def qtob(num):
    return ("%016x" % (num & 0xFFFFFFFFFFFFFFFF)).decode("hex")

def ltoi(mem):
    return int(mem[::-1].encode("hex"), 16)

def btoi(mem):
    return int(mem.encode("hex"), 16)

def sopr(a, b, f):
    t = max(len(a), len(b))
    return "".join([chr(f(ord(a.ljust(t, "\x00")[i]), ord(b.ljust(t, "\x00")[i]))) for i in xrange(t)])

def sand(a, b):
    return sopr(a, b, operator.and_)

def sor(a, b):
    return sopr(a, b, operator.or_)

def sxor(a, b):
    return sopr(a, b, operator.xor)

def sinv(a):
    return "".join([chr(ord(i) ^ 0xff) for i in a])
