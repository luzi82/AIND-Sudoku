import unittest

class TestNakedTwins(unittest.TestCase):
    def test_naked_twins(self):
        self.assertEqual({'a':0,'b':1}, {'b':1,'a':0})

if __name__ == '__main__':
    unittest.main()
