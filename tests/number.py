import unittest
import random
from pwnbox import number

class TestMath(unittest.TestCase):
    def test_power(self):
        for i in xrange(10):
            x, y, m = random.randint(1, 1000000), random.randint(1, 1000), random.randint(2, 1000000)
            self.assertEqual(number.power(x, y), x ** y)
            self.assertEqual(number.power(x, y, m), (x ** y) % m)

class TestPrime(unittest.TestCase):
    def primetest(self, n):
        x = 2
        while x * x <= n:
            if n % x == 0:
                return False
            x += 1
        return True

    def test_MillerRabin(self):
        for i in xrange(10):
            x = random.randint(1, 10 ** 6)
            self.assertEqual(number.MillerRabin(x), self.primetest(x))

    def test_prange(self):
        for i in xrange(10):
            x = random.randint(1, 10 ** 5)
            t = []
            for i in xrange(x, x + 10):
                if self.primetest(i):
                    t.append(i)
            self.assertEqual(list(number.prange(x, x + 10)), t)

    def test_prime(self):
        for i in xrange(10):
            x = random.randint(1, 10 ** 6)
            self.assertEqual(number.prime(x), self.primetest(x))

class TestModular(unittest.TestCase):
    def test_gcd(self):
        self.assertEqual(number.gcd(12, 18), 6)
        self.assertEqual(number.gcd(36, 11), 1)
        self.assertEqual(number.gcd(14, 7), 7)

    def test_egcd(self):
        for i in xrange(10):
            x, y = random.randint(1, 10 ** 12), random.randint(1, 10 ** 12)
            g, a, b = number.egcd(x, y)
            self.assertEqual(x * a + y * b, g)

    def test_modinv(self):
        for i in xrange(10):
            x = y = 0
            while number.gcd(x, y) != 1:
                x, y = random.randint(1, 10 ** 12), random.randint(1, 10 ** 12)
            self.assertEqual((number.modinv(x, y) * x) % y, 1)

    def test_ChineseRemainderTheorem(self):
        for i in xrange(10):
            n = random.randint(1, 10)
            x = random.randint(1, 10 ** 12)
            r = [random.randint(1, 10 ** 8) for i in xrange(n)]
            q = [x % i for i in r]
            y = number.ChineseRemainderTheorem(q, r)
            for z, w in zip(q, r):
                self.assertEqual(y % w, z)
