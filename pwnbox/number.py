"""Number theory algorithms.
"""

from functools import reduce, wraps

try:
    xrange
except NameError:
    xrange = range

has_gmpy2 = False
try:
    import gmpy2
    has_gmpy2 = True
except ImportError:
    pass

def gmpy2_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not has_gmpy2:
            raise ImportError("gmpy2 is required")
        return func(*args, **kwargs)
    return wrapper

@gmpy2_required
def crt(remainders, moduli, coprime = True):
    """Chinese Remainder Theorem.

    :param remainders: list of remainders.
    :param moduli: list of modulies.
    :param coprime: (optional) set ``False`` if modulies are not coprimes.
    """
    if not coprime:
        iternums = iter(zip(remainders, moduli))
        v, m = next(iternums)
        for u, n in iternums:
            g, s, t = gmpy2.gcdext(m, n)
            assert(v % g == u%g)
            v += s * m // g * (u - v)
            m *= n // g
        return (v % m, m)

    p = reduce(lambda x, y : x * y, moduli)
    v = 0
    for u, m in zip(remainders, moduli):
        e = p // m
        g, s, t = gmpy2.gcdext(e, m)
        v += e * (u * s % m)
    return (v % p, p)

@gmpy2_required
def cf(n, m):
    """Rational number ``n // m`` to continued fraction.

    :param n: numerator.
    :param m: denominator.
    """
    res = []
    while m:
        x = gmpy2.f_div(n, m)
        res.append(x)
        n, m = m, n - m * x
    return res

@gmpy2_required
def cf_convergents(cf):
    """Continued fraction to convergents

    :param cf: continued fraction.
    """
    assert(has_gmpy2)
    p_2, q_2 = gmpy2.mpz(0), gmpy2.mpz(1)
    p_1, q_1 = gmpy2.mpz(1), gmpy2.mpz(0)
    res = []
    for x in cf:
        p, q = x * p_1 + p_2, x * q_1 + q_2
        p_2, q_2 = p_1, q_1
        p_1, q_1 = p, q
        res.append((p, q))
    return res

@gmpy2_required
def wiener_attack(N, e):
    """Perform Wiener's attack.

    :param N: RSA public key N.
    :param e: RSA public key e.
    """
    convergents = cf_convergents(cf(e, N))
    for k,d in convergents:
        if k == 0 or (e * d - 1) % k != 0:
            continue
        phi = (e * d - 1) // k
        c = N - phi + 1
        # now p,q can be the root of x**2 - s*x + n = 0
        det = c * c - 4 * N
        if not det >= 0:
            continue
        s, r = gmpy2.isqrt_rem(det)
        if r == 0 and gmpy2.is_even(c + s):
            return (d, (c + s) // 2,(c - s) // 2)
    # Failed
    return None

@gmpy2_required
def fermat_factoring(N, trial = 1 << 32):
    """Perform Fermat's factorization.

    :param N: number to factorize.
    :param trial: (optional) maximum trial number.
    """
    x = gmpy2.isqrt(N) + 1
    y = x * x - N
    for i in xrange(trial):
        if gmpy2.is_square(y):
            y = gmpy2.isqrt(y)
            return (x + y,x - y)
        y += (x << 1) + 1
        x += 1
    # Failed
    return None

@gmpy2_required
def pollard_rho(n):
    """Pollard's rho method for small prime factor.

    :param N: number to factorize.
    """
    def g(x, n):
        return (x**2 + 1) % n

    x, y, d = 2, 2, 1
    while d == 1:
        x = g(x, n)
        y = g(g(y, n), n)
        d = gmpy2.gcd(x - y, n)

    if d != n:
        return d, n // d

    # Failed
    return None

