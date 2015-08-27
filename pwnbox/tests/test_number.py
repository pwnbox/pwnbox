import unittest
import imp
import pwnbox
import random
import gmpy2
from Crypto.Util.number import getPrime
class TestImport(unittest.TestCase):
    def test_has_gmpy2(self):
        has_gmpy2 = False
        try:
            imp.find_module('gmpy2')
            has_gmpy2 = True
        except ImportError:
            pass
        if has_gmpy2:
            try:
                pwnbox.number
            except AttributeError:
                self.fail('pwnbox.number not imported with gmpy2')
        else:
            with self.assertRaises(AttributeError):
                pwnbox.number

class TestNumber(unittest.TestCase):
    def test_crt_coprime(self):
        v = random.randint(10,10000000000)
        n = random.randint(1,100)
        remainders = []
        moduli = []
        lcm = 1
        for i in range(n):
            while True:
                mod = random.randint(2,100000000)
                g = gmpy2.gcd(mod,lcm)
                if g == 1 : break
            remainders.append(v%mod)
            moduli.append(mod)
            lcm*=mod
        res = pwnbox.number.crt(remainders,moduli)
        self.assertEqual(res,(v%lcm,lcm))

    def test_crt_without_coprime(self):
        v = random.randint(10,10000000000)
        n = random.randint(1,100)
        remainders = []
        moduli = []
        for i in range(n):
            mod = random.randint(2,100000000)
            remainders.append(v%mod)
            moduli.append(mod)
        lcm = reduce(gmpy2.lcm,moduli)
        res = pwnbox.number.crt(remainders,moduli,False)
        self.assertEqual(res,(v%lcm,lcm))

    def test_fermat_factoring(self):
        q = getPrime(512)
        p = gmpy2.next_prime(q + random.randint(1<<64,1<<128))
        self.assertEqual((p,q),pwnbox.number.fermat_factoring(p*q))

    def test_wiener(self):
        q = gmpy2.mpz(getPrime(512))
        p = gmpy2.mpz(getPrime(512))
        if q>p :
            p,q = q,p
        n = p*q
        phi = (p-1)*(q-1)
        d = gmpy2.iroot(n,5)[0]
        while gmpy2.gcd(d,phi) != 1 :
            d -= 1
        e = gmpy2.invert(d,phi)
        self.assertEqual((d,p,q),pwnbox.number.wiener_attack(n,e))
