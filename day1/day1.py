def calculate_fuel(modules):
    total = 0
    for module in modules:
        fuel = int(float(module) / 3) - 2
        print(f'Module mass: {module} -- Fuel for module: {fuel}')
        total += fuel
    return total


def fuel_for_module(module):
    fuel = fuel_for_mass(module)
    print(f'Module mass: {module} -- Total fuel required: {fuel}')
    return fuel


def fuel_for_mass(mass):
    fuel = int(float(mass) / 3) - 2
    if fuel <= 0:
        return 0
    else:
        return fuel + fuel_for_mass(fuel)


def day1pt1(path):
    file = open(path)
    modules = []
    for line in file:
        modules.append(line.strip())
    return calculate_fuel(modules)


def day1pt2(path):
    file = open(path)
    modules = []
    for line in file:
        modules.append(line.strip())
    # And now to get totals...
    total = 0
    for module in modules:
        total += fuel_for_module(module)
    return total


if __name__ == "__main__":
    z = day1pt2('modules.txt')
    print(f'Total fuel required for given modules: {z}')
    test = [12, 14, 1969, 100756]
    for x in test:
        fuel_for_module(x)
