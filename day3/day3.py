from typing import List


class Wire:
    def __init__(self, raw_path: str):
        self.node_list = []
        self.sorted_nodes = []
        self.raw_path = raw_path.split(',')
        self.x = 0
        self.y = 0

    def run_path(self):
        self.x = 0
        self.y = 0
        self.node_list = []  # Reset - 0, 0 not added

        directions = {
            'U': (0, 1),
            'R': (1, 0),
            'D': (0, -1),
            'L': (-1, 0)
        }
        for move in self.raw_path:
            direction = directions.get(move[0])
            distance = int(move[1:])
            for i in range(distance):
                self.x += direction[0]  # X-position manipulation
                self.y += direction[1]  # Y-"       "       "
                self.node_list.append((self.x, self.y))
                #print(f'Added {self.x}, {self.y} to path')


class Wiregrid:
    def __init__(self, wires: List[Wire]):
        self.wires = wires

    def run_wires(self):
        for wire in self.wires:
            wire.run_path()

    def distance_to_closest_crossing(self) -> int:
        crossings = self.get_crossings()
        if len(crossings) == 0:
            raise Exception('No crossings found')
        min_distance = abs(crossings[0][0]) + abs(crossings[0][1])
        for cross in crossings[1:]:
            distance_to_cross = abs(cross[0]) + abs(cross[1])
            if distance_to_cross < min_distance:
                min_distance = distance_to_cross
                # print(f'cross {cross} wins now with {min_distance}')
        return min_distance

    def wire_distance_to_closest_crossing(self) -> int:
        crossings = self.get_crossings()
        shortest_path = 9999999
        for cross in crossings:
            w0_dist = 0
            w1_dist = 0
            while self.wires[0].node_list[w0_dist] != cross:
                w0_dist += 1
            while self.wires[1].node_list[w1_dist] != cross:
                w1_dist += 1
            if w0_dist + w1_dist < shortest_path:
                shortest_path = w0_dist + w1_dist
        return shortest_path + 2        # Accounting for the move from the origin to the first node

    def get_crossings(self):
        crossings = list(set(self.wires[0].node_list).intersection(self.wires[1].node_list))
        # print(f'Crossings: {crossings}\nCount: {len(crossings)}')
        return crossings


if __name__ == '__main__':
    wire_paths = open('input.txt').read().strip().split('\n')
    wire_list = []
    for path in wire_paths:
        wire_list.append(Wire(path))
    wire_grid = Wiregrid(wire_list)
    wire_grid.run_wires()
    print(f'Day 3 Part 1 result (closest crossing): {wire_grid.distance_to_closest_crossing()}')
    print(f'Day 3 Part 2 result (shortest path): {wire_grid.wire_distance_to_closest_crossing()}')
