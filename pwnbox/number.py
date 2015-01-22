def power(x, y, m = 0):
    if y == 0:
        return 1
    z = power(x, y >> 1, m)
    z = (z * z) % m if m else z * z
    if y & 1:
        z = (z * x) % m if m else z * x
    return z

def MillerRabin(n):
    MillerRabin.maxn = 3825123056546413051
    if n <= 1:
        return False
    a = [2, 3, 5, 7, 11, 13, 17, 19, 23]
    m = n - 1
    s = 0
    while m & (1 << s) == 0:
        s += 1
    for i in a:
        if n <= i:
            break
        if power(i, m >> s, n) == 1:
            continue
        for j in xrange(1, s + 1):
            if power(i, m >> j, n) == m:
                break
        else:
            return False
    return True
