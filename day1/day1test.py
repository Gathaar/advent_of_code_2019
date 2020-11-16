import unittest
from day1 import Module, FCU


class Day1Tests(unittest.TestCase):
    def test_part1(self):
        mod0 = Module(12)
        self.assertEqual(2, mod0.get_fuel_simple())
        mod1 = Module(14)
        self.assertEqual(2, mod1.get_fuel_simple())
        mod2 = Module(1969)
        self.assertEqual(654, mod2.get_fuel_simple())
        mod3 = Module(100756)
        self.assertEqual(33583, mod3.get_fuel_simple())
        mod_list = [mod0, mod1, mod2, mod3]
        fuel_counter = FCU(mod_list)
        self.assertEqual(34241, fuel_counter.get_total_fuel_simple())

    def test_part2(self):
        mod1 = Module(14)
        self.assertEqual(2, mod1.get_fuel())
        mod2 = Module(1969)
        self.assertEqual(966, mod2.get_fuel())
        mod3 = Module(100756)
        self.assertEqual(50346, mod3.get_fuel())


if __name__ == '__main__':
    unittest.main()
