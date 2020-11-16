import unittest
from day3 import Wire, Wiregrid


class Day3Test(unittest.TestCase):
    def test_p1_0(self):
        test0_wire0 = Wire('R75,D30,R83,U83,L12,D49,R71,U7,L72')
        test0_wire1 = Wire('U62,R66,U55,R34,D71,R55,D58,R83')
        test0_grid = Wiregrid([test0_wire0, test0_wire1])
        test0_grid.run_wires()
        self.assertEqual(159, test0_grid.distance_to_closest_crossing())

    def test_p1_1(self):
        test1_wire0 = Wire('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51')
        test1_wire1 = Wire('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7')
        test1_grid = Wiregrid([test1_wire0, test1_wire1])
        test1_grid.run_wires()
        self.assertEqual(135, test1_grid.distance_to_closest_crossing())

    def test_p2_0(self):
        test0_wire0 = Wire('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51')
        test0_wire1 = Wire('U98,R91,D20,R16,D67,R40,U7,R15,U6,R7')
        test0_grid = Wiregrid([test0_wire0, test0_wire1])
        test0_grid.run_wires()
        self.assertEqual(410, test0_grid.wire_distance_to_closest_crossing())

    def test_p2_1(self):
        test1_wire0 = Wire('R75,D30,R83,U83,L12,D49,R71,U7,L72')
        test1_wire1 = Wire('U62,R66,U55,R34,D71,R55,D58,R83')
        test1_grid = Wiregrid([test1_wire0, test1_wire1])
        test1_grid.run_wires()
        self.assertEqual(610, test1_grid.wire_distance_to_closest_crossing())


if __name__ == '__main__':
    unittest.main()
