# Day 6: Celestial Bodies: what do they stick to?
#   - input is a list of max 3-char "body names", a closeparen and a second max 3-char "body name"
#   - format: XXX)YYY   => XXX is orbited by YYY
#   - obviously points to a tree construct -- the input doesn't provide a root of any kind however
#   - building the tree and ordering it will likely be the hardest part

import unittest
from typing import List, Any, Union


class UniverseSandbox3(unittest.TestCase):
    # Can bad class names be copyright claimed?
    def test_creation(self):
        galactic_map = [
            ['CTR', 'A'],
            ['B', 'C'],
            ['CTR', 'B']
        ]
        universe = OrbitalMap(galactic_map)
        self.assertEqual(1, len(universe.roots))  # the universe should have 1 root: CTR

    def test_2(self):
        test_input = process_raw(open('test2.txt', 'r').read())
        universe = OrbitalMap(test_input)
        self.assertEqual(1, len(universe.roots))

    def test_3(self):
        # Tests multiple roots eventually merging
        test_input = process_raw(open('test3.txt', 'r').read())
        universe = OrbitalMap(test_input)
        self.assertEqual(1, len(universe.roots))

    def test_4(self):
        # Tests using actual input data whether forming the universe works out
        test_input = process_raw(open('input.txt', 'r').read())
        universe = OrbitalMap(test_input)
        self.assertEqual(1, len(universe.roots))

    def test_creation_2(self):
        galactic_map = [
            ['CTR', 'A'],
            ['B', 'C'],
            ['CTR', 'B']
        ]
        universe = OrbitalMap(galactic_map)
        self.assertEqual(4, universe.get_depth())  # the universe should have 1 root: CTR

    def test_depth_finder(self):
        galactic_map = [
            ['C', 'abc'],
            ['abc', 'def'],
            ['def', 't'],
            ['def', 'y']
        ]
        universe = OrbitalMap(galactic_map)
        self.assertEqual(9, universe.get_depth())

    def test_depth_finder_2(self):
        test_input = process_raw(open('test2.txt', 'r').read())
        universe = OrbitalMap(test_input)
        self.assertEqual(42, universe.get_depth())

    def test_IMCOMINGSANTA(self):
        test_input = process_raw((open('test4.txt', 'r').read()))
        universe = OrbitalMap(test_input)
        self.assertEqual(4, universe.hops_to_santa())


class CelestialBody:
    # Themed name for a node struct
    orbits = None
    orbited_by = []  # TIL orbited by is correct, orbitTed is not

    def __init__(self, name, **kwargs):
        self.name = name
        # https://stackoverflow.com/questions/8187082/how-can-you-set-class-attributes-from-variable-arguments-kwargs-in-python
        for key, value in kwargs.items():
            setattr(self, key, value)  # allows for dynamic binding

    def add_orbiter(self, orbiter):
        self.orbited_by.append(orbiter)

    def __str__(self):
        return self.name


class OrbitalMap:
    roots = []  # any celestial body who does not (yet) orbit another
    in_existence = []

    def __init__(self, celestial_map):
        # build celestial tree
        self.generate_universe(celestial_map)

    def generate_universe(self, celestial_map):
        # Expected input: list of tuples; 0 being the orbited body, 1 being the orbiter
        #   First tuple will be a (temporary?) root - child either way
        original_root = CelestialBody(celestial_map[0][0])
        original_orbiter = CelestialBody(celestial_map[0][1], orbits=original_root, orbited_by=[])
        original_root.orbited_by.append(original_orbiter)
        self.roots.append(original_root)
        self.in_existence.append(original_root.name)
        self.in_existence.append(original_orbiter.name)

        #print(f'Original orbiter orbiters: {original_orbiter.orbited_by}')

        for center, orbiter in celestial_map[1:]:
            # Find (or create) the center
            #print(f'Handling body: {center} with orbiter: {orbiter}')
            center_body = None

            if center in self.in_existence:
                for constellation in self.roots:
                    center_body = self.find_body(constellation, center)
                    if center_body:
                        # Found it, stop looping
                        break
            else:
                # The center is a new body - SHAPE THE UNIVERSE!
                #print(f'Center body wasn\'t found, adding {center} to the universe')
                center_body = CelestialBody(center, orbits=None, orbited_by=[])
                self.roots.append(center_body)
                self.in_existence.append(center)

            # Find (or create) the orbiter
            orbiter_body = None

            if orbiter in self.in_existence:
                for constellation in self.roots:
                    # print(f'Looking for body {orbiter} in constellation root {constellation.name}')
                    orbiter_body = self.find_body(constellation, orbiter)
                    if orbiter_body:
                        break
                center_body.add_orbiter(orbiter_body)
                # print(f'Appended {orbiter_body} to orbits for {center_body}')
                orbiter_body.orbits = center_body  # may be unnecessary (as it should be discoverable top-down)
                # If this body was in the roots - discard it... it has a new root now!
                for body in self.roots:
                    if body.name == orbiter_body.name:
                        self.roots.remove(body)
                        #print(f'Removed {body} from roots')
            else:
                # A whole new wooooooorld
                orbiter_body = CelestialBody(orbiter, orbits=center_body, orbited_by=[])
                center_body.orbited_by.append(orbiter_body)
                #print(f'Created body {orbiter_body} as it didn\'t exist!\n'
                #      f'Also attached it to the orbits of {center_body}')
                self.in_existence.append(orbiter_body.name)

    def find_body(self, body: CelestialBody, to_find: str):
        if body.name == to_find:
            #print(f'Found {body.name}!')
            return body

        if not body.orbited_by:
            # print(f'{body.name} ain\'t got no orbits')
            return None

        #print(f'Preparing to look in the orbiters of {body.name} - there are {len(body.orbited_by)}')
        for orbiter in body.orbited_by:
            #print(f'Found orbiter {orbiter.name} around {body.name}')
            result = self.find_body(orbiter, to_find)
            if result is not None:
                # print(f'Found a hit! Bubbling... Body is {body}')
                return result
            else:
                # print(f'Dead trail...')
                pass

        return None

    def get_depth(self):
        print(f'\n\n\t -- DEPTH FINDER 9000 --')
        return self.depth_of_the_universe(self.roots[0])[0]

    def depth_of_the_universe(self, body):
        subtotal = 0
        children = 1
        for orbiter in body.orbited_by:
            deeper = self.depth_of_the_universe(orbiter)
            subtotal += deeper[0] + deeper[1]
            children += deeper[1]

        #print(f'Returning {subtotal}/{children} for {body}')
        return [subtotal, children]

    def hops_to_santa(self):
        # Map (to center) for YOU (= me)
        my_map_to_center: List[CelestialBody] = []
        my_body = self.find_body(self.roots[0], 'YOU')
        body = my_body
        while body.name != self.roots[0].name:
            my_map_to_center.append(body)
            body = body.orbits

        # Map (to center) for SANta
        santa_map_to_center = []
        santa_body = self.find_body(self.roots[0], 'SAN')
        body = santa_body
        while body.name != self.roots[0].name:
            santa_map_to_center.append(body)
            body = body.orbits

        # Find the nearest link to santa
        nearest_jump = None
        for o in reversed(my_map_to_center):
            if o in santa_map_to_center:
                nearest_jump = o

        my_distance_to_jump = my_map_to_center.index(nearest_jump)
        santa_distance_to_jump = santa_map_to_center.index(nearest_jump)
        return my_distance_to_jump + santa_distance_to_jump - 2     # - 2 as "only the orbit need be altered"


def process_raw(raw_input: str):
    intermediate_result = raw_input.replace(' ', '').split('\n')
    result = []
    for item in intermediate_result:
        split_item = item.split(')')
        result.append([split_item[0], split_item[1]])

    return result


if __name__ == '__main__':
    print(f'Galactic map initializing...')
    universe = OrbitalMap(process_raw(open('input.txt', 'r').read()))
    print(f'PART 1 RESULT: {universe.get_depth()}')
    print(f'PART 2 RESULT: {universe.hops_to_santa()}')
