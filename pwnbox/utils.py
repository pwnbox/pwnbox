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
