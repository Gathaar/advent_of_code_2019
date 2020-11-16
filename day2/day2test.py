import unittest
from day2 import Intcode


class Day2Test(unittest.TestCase):
    def test_part1(self):
        program0 = [1, 0, 0, 0, 99]
        test0 = Intcode(program0)
        test0.run()
        self.assertEqual([2, 0, 0, 0, 99], test0.__str__())

        program1 = [2, 3, 0, 3, 99]
        test1 = Intcode(program1)
        test1.run()
        self.assertEqual([2, 3, 0, 6, 99], test1.__str__())

        program2 = [2, 4, 4, 5, 99, 0]
        test2 = Intcode(program2)
        test2.run()
        self.assertEqual([2, 4, 4, 5, 99, 9801], test2.__str__())

        program3 = [1, 1, 1, 4, 99, 5, 6, 0, 99]
        test3 = Intcode(program3)
        test3.run()
        self.assertEqual([30, 1, 1, 4, 2, 5, 6, 0, 99], test3.__str__())


if __name__ == '__main__':
    unittest.main()
