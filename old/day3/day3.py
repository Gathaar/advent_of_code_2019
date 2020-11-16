import unittest
from operator import itemgetter


class Day3Test(unittest.TestCase):
    def test_part1_1(self):
        raw_input = 'R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83'
        self.assertEqual(159, day3part1(raw_input))

    def test_part1_2(self):
        raw_input = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
        self.assertEqual(135, day3part1(raw_input))

    def test_part2_1(self):
        raw_input = 'R75,D30,R83,U83,L12,D49,R71,U7,L72\nU62,R66,U55,R34,D71,R55,D58,R83'
        self.assertEqual(610, day3part2(raw_input))

    def test_part2_2(self):
        raw_input = 'R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51\nU98,R91,D20,R16,D67,R40,U7,R15,U6,R7'
        self.assertEqual(410, day3part2(raw_input))


class Wire:
    def __init__(self, raw_input):
        # We get a path, let's build this wire
        self.path = [[0, 0]]
        x = 0   # "LEFT - RIGHT"
        y = 0   # "UP - DOWN"
        for maneuver in raw_input.split(','):
            if maneuver[0] == 'U':
                # UP
                for i in range(int(maneuver[1:])):
                    y += 1
                    self.path.append([x, y])
            elif maneuver[0] == 'D':
                # DOWN
                for i in range(int(maneuver[1:])):
                    y -= 1
                    self.path.append([x, y])
            elif maneuver[0] == 'L':
                # LEFT
                for i in range(int(maneuver[1:])):
                    x -= 1
                    self.path.append([x, y])
            elif maneuver[0] == 'R':
                # RIGHT
                for i in range(int(maneuver[1:])):
                    x += 1
                    self.path.append([x, y])
            else:
                # PANIC
                print(f'Found |{maneuver}| and stumbled')


def get_crossovers(wire1: Wire, wire2: Wire):
    crossovers = []
    w1_path = wire1.path[1:].copy()
    w2_path = wire2.path[1:].copy()
    w1_path.sort(key=itemgetter(1))  # pre-sort by y
    w1_path.sort(key=itemgetter(0))  # sort by x value
    w2_path.sort(key=itemgetter(1))
    w2_path.sort(key=itemgetter(0))  # sort by x value

    for w1_node in w1_path:
        for w2_node in w2_path:
            if w1_node[0] == w2_node[0]:
                # x is equal
                if w1_node[1] == w2_node[1]:
                    # y, too, is equal!
                    crossovers.append(w1_node)
            elif w1_node[0] < w2_node[0]:
                break
        w2_path = w2_path[1:]  # Reduce complexity - as lists are sorted this won't need to be checked again
        #print(f'Length remaining: {len(w2_path)}')

    return crossovers


def cross_reference(wire1: Wire, wire2: Wire):
    # Clever name, giggity
    # Returns distance to 0,0 (manhattan distance)
    crossovers = get_crossovers(wire1, wire2)

    # check minimum distance
    min_distance = 999999    # arbitrarily large, right?
    for node in crossovers:
        node_distance = abs(node[0]) + abs(node[1])
        if node_distance < min_distance:
            min_distance = node_distance
    return min_distance


def shortest_signal_distance(wire1: Wire, wire2: Wire):
    crossovers = get_crossovers(wire1, wire2)
    shortest_signal = 999999    # arbitrarily large
    for crossing in crossovers:
        i = 0
        j = 0
        while wire1.path[i] != crossing:
            i += 1
        while wire2.path[j] != crossing:
            j += 1
        print(f'Distance to crossing at x:{crossing[0]}/y:{crossing[1]} reached in following distances:\n\t'
              f'- Wire 1: {i}\n\t- Wire 2: {j}')
        if i + j < shortest_signal:
            print(f'\t !! NEW RECORD -- {i + j} !!')
            shortest_signal = i + j
    return shortest_signal

def day3part1(raw_input):
    wire1 = Wire(raw_input.split('\n')[0])
    wire2 = Wire(raw_input.split('\n')[1])
    return cross_reference(wire1, wire2)


def day3part2(raw_input):
    wire1 = Wire(raw_input.split('\n')[0])
    wire2 = Wire(raw_input.split('\n')[1])
    return shortest_signal_distance(wire1, wire2)


if __name__ == '__main__':
    raw_input = open('input.txt', 'r').read()

    # Part 1
    # print(f'Solution for day 3 part 1: {day3part1(raw_input)}')

    # Part 2
    print(f'Solution for day 3 part 2: {day3part2(raw_input)}')
