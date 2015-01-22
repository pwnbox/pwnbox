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
            x = random.randint(1, 1000000)
            self.assertEqual(number.MillerRabin(x), self.primetest(x))

    def test_prange(self):
        for i in xrange(10):
            x = random.randint(1, 100000)
            t = []
            for i in xrange(x, x + 10):
                if self.primetest(i):
                    t.append(i)
            self.assertEqual(list(number.prange(x, x + 10)), t)

    def test_prime(self):
        for i in xrange(10):
            x = random.randint(1, 1000000)
            self.assertEqual(number.prime(x), self.primetest(x))
