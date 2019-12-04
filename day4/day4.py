#   Day 4 part 1: rules
#       - 6 digits
#       - given range
#       - digits only INCREASE (0 => 9)
#       - 1 double MUST be present


import unittest


class Day4Tests(unittest.TestCase):
    def test_is_valid(self):
        self.assertEqual(False, is_valid_1(543210))
        self.assertEqual(False, is_valid_1(123456))
        self.assertEqual(True, is_valid_1(123345))
        # Actual examples listed on page
        self.assertEqual(True, is_valid_1(111111))
        self.assertEqual(False, is_valid_1(223450))
        self.assertEqual(False, is_valid_1(123789))

    def test_is_valid_2(self):
        self.assertEqual(True, is_valid_2(112233))
        self.assertEqual(False, is_valid_2(123444))
        self.assertEqual(True, is_valid_2(111122))


def is_valid_1(password: int):
    # map to int, then list
    number_list = list(map(int, str(password)))

    if len(number_list) != 6:
        return False
    i = 0       # loop counter
    has_double = False

    for i in range(len(number_list) - 1):
        if number_list[i] > number_list[i+1]:
            return False
        elif number_list[i] == number_list[i+1]:
            has_double = True

    return has_double


def is_valid_2(password):
    # map to int, then list
    number_list = list(map(int, str(password)))

    if len(number_list) != 6:
        return False
    i = 0  # loop counter
    has_double = False

    for i in range(len(number_list) - 1):
        if number_list[i] > number_list[i + 1]:
            return False
        elif number_list[i] == number_list[i + 1]:
            has_double = True

    if has_double:
        # Check for an element's count to be EXACTLY 2
        for i in number_list:
            if number_list.count(i) == 2:
                return True
    return False


def day4part1(minimum: int, maximum: int):
    i = minimum
    counter = 0

    while i <= maximum:
        if is_valid_1(i):
            counter += 1
        i += 1

    return counter


def day4part2(minimum: int, maximum: int):
    i = minimum
    counter = 0

    while i <= maximum:
        if is_valid_2(i):
            counter += 1
        i += 1

    return counter


if __name__ == "__main__":
    lower_bound = 197487
    upper_bound = 673251

    solution_part_1 = day4part1(lower_bound, upper_bound)
    solution_part_2 = day4part2(lower_bound, upper_bound)

    print(f'Solution for part 1: {solution_part_1} valid passwords.\n'
          f'Solution for part 2: {solution_part_2} valid passwords.')
