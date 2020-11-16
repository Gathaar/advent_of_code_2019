from math import floor
from typing import List


class Module:
    def __init__(self, mass: int):
        self.mass = mass

    def get_fuel_simple(self) -> int:
        return floor(self.mass / 3) - 2

    def get_fuel(self) -> int:
        return self.fuel_per_mass(self.mass)

    def fuel_per_mass(self, mass) -> int:
        to_return = floor(mass / 3) - 2
        if to_return <= 0:
            return 0
        else:
            return to_return + self.fuel_per_mass(to_return)


# Fuel Counter-Upper
class FCU:
    modules = []

    def __init__(self, modules: List[Module]):
        self.modules = modules

    def get_total_fuel_simple(self) -> int:
        total = 0
        for module in self.modules:
            total += module.get_fuel_simple()

        return total

    def get_total_fuel(self) -> int:
        total = 0
        for module in self.modules:
            total += module.get_fuel()

        return total


if __name__ == '__main__':
    file = open('input.txt')
    mods = []
    for line in file:
        temp = Module(int(line.strip()))
        mods.append(temp)
    fuel_counter_upper = FCU(mods)
    print(f'Day 1 Part 1 result (based on input.txt): {fuel_counter_upper.get_total_fuel_simple()}')
    print(f'Day 1 Part 2 result (based on input.txt): {fuel_counter_upper.get_total_fuel()}')
