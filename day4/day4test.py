import unittest
from day4 import Validator


class Day4Test(unittest.TestCase):
    def test_part1_0(self):
        v = Validator()
        self.assertEqual(True, v.is_valid(password='111111'))

    def test_part1_1(self):
        v = Validator()
        self.assertEqual(False, v.is_valid(password='223450'))

    def test_part1_2(self):
        v = Validator()
        self.assertEqual(False, v.is_valid(password='123789'))


if __name__ == '__main__':
    unittest.main()
