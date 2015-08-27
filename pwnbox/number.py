import gmpy2

def crt(remainders, moduli, coprime = True):
    assert(len(remainders) == len(moduli))
    if not coprime:
        v, m = remainders[0], moduli[0]
        for u, n in zip(remainders, moduli)[1:]:
            g,s,t = gmpy2.gcdext(m,n)
            assert(v%g == u%g)
            v += s*m/g*(u-v)
            m*= n/g
        return (v%m,m)

    p = reduce(lambda x,y : x*y,moduli)
    v = 0
    for u, m in zip(remainders, moduli):
        e = p / m
        g, s, t = gmpy2.gcdext(e, m)
        v += e*(u*s % m)
    return (v%p,p)

def q2cf(n, m):
    """
    convert rational number n/m to continued fraction.
    """
    res = []
    while m:
        x = gmpy2.f_div(n, m)
        res.append(x)
        n, m = m, n-m*x
    return res

def cf_convergents(cf):
    """
    convert continued fraction to convergents.
    """
    p_2, q_2 = gmpy2.mpz(0), gmpy2.mpz(1)
    p_1, q_1 = gmpy2.mpz(1), gmpy2.mpz(0)
    res = []
    for x in cf:
        p, q = x*p_1 + p_2, x*q_1 + q_2
        p_2,q_2 = p_1,q_1
        p_1,q_1 = p,q
        res.append((p,q))
    return res

def wiener_attack(N,e):
    convergents = cf_convergents(q2cf(e,N))
    for k,d in convergents:
        if k==0 or (e*d-1)%k != 0:
            continue
        phi = (e*d-1)/k
        c = N - phi + 1
        # now p,q can be the root of x**2 - s*x + n = 0
        det = c*c - 4*N
        if not det >= 0:
            continue
        s, r = gmpy2.isqrt_rem(det)
        if r==0 and gmpy2.is_even(c+s):
            return (d,(c+s)/2,(c-s)/2)
    # Failed
    return None

def fermat_factoring(N,trial=1<<32):
    x = gmpy2.isqrt(N)+1
    y = x*x - N
    for i in xrange(trial):
        if gmpy2.is_square(y):
            y = gmpy2.isqrt(y)
            return (x+y,x-y)
        y += (x<<1)+1
        x += 1
    # Failed
    return None
