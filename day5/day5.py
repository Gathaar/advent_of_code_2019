import unittest
from unittest import mock


class TestMeBaby(unittest.TestCase):
    # Re-runs day 2's tests to ensure te program can handle it all
    def test_day2(self):
        test = [[[1, 0, 0, 0, 99], [2, 0, 0, 0, 99]],
                [[2, 3, 0, 3, 99], [2, 3, 0, 6, 99]],
                [[2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]],
                [[1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]]]
        for case in test:
            computer = Intcode(case[0])
            computer.run_program()
            self.assertEqual(case[1], computer.instruction_set)

    def test_input_output(self):
        test = [3, 0, 4, 0, 99]
        computer = Intcode(test)
        with mock.patch('builtins.input', return_value="1"):
            computer.run_program()
            self.assertEqual("1", computer.output)

    def test_part2_case1(self):
        computer = Intcode([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8])
        with mock.patch('builtins.input', return_value="8"):
            computer.run_program()
            self.assertEqual("1", computer.output)

        with mock.patch('builtins.input', return_value="0"):
            computer.run_program()
            self.assertEqual("0", computer.output)

    def test_part2_case2(self):
        computer = Intcode([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8])
        with mock.patch('builtins.input', return_value="0"):
            computer.run_program()
            self.assertEqual("1", computer.output)

        with mock.patch('builtins.input', return_value="9"):
            computer.run_program()
            self.assertEqual("0", computer.output)

    def test_part2_case3(self):
        computer = Intcode([3, 3, 1108, -1, 8, 3, 4, 3, 99])
        with mock.patch('builtins.input', return_value="8"):
            computer.run_program()
            self.assertEqual("1", computer.output)

        with mock.patch('builtins.input', return_value="1"):
            computer.run_program()
            self.assertEqual("0", computer.output)

    def test_part2_case4(self):
        computer = Intcode([3, 3, 1107, -1, 8, 3, 4, 3, 99])
        with mock.patch('builtins.input', return_value="1"):
            computer.run_program()
            self.assertEqual("1", computer.output)

        with mock.patch('builtins.input', return_value="9"):
            computer.run_program()
            self.assertEqual("0", computer.output)

    def test_part2_case5(self):
        computer = Intcode([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9])
        with mock.patch('builtins.input', return_value="0"):
            computer.run_program()
            self.assertEqual("0", computer.output)

        with mock.patch('builtins.input', return_value="8"):
            computer.run_program()
            self.assertEqual("1", computer.output)

    def test_part2_case6(self):
        computer = Intcode([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1])
        with mock.patch('builtins.input', return_value="8"):
            computer.run_program()
            self.assertEqual("1", computer.output)

        with mock.patch('builtins.input', return_value="0"):
            computer.run_program()
            self.assertEqual("0", computer.output)

    def test_part2_case7(self):
        computer = Intcode([3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                            1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                            999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99])
        with mock.patch('builtins.input', return_value="0"):
            computer.run_program()
            self.assertEqual("999", computer.output)

        with mock.patch('builtins.input', return_value="8"):
            computer.run_program()
            self.assertEqual("1000", computer.output)

        with mock.patch('builtins.input', return_value="9"):
            computer.run_program()
            self.assertEqual("1001", computer.output)


# Custom exception to halt without extra trouble
class ForceHalt(Exception):
    pass


# noinspection SpellCheckingInspection
class Intcode:
    pos = None
    output = None

    def __init__(self, instruction_set):
        # Assume the instruction_set is a list (or at least iterable) of ints
        print(f'\t. . . InItIaLiZiNg . . .')
        self.instruction_set = instruction_set
        self.opcodes = {
            1: self.add,
            2: self.multiply,
            3: self.get_input,
            4: self.put_output,
            5: self.jump_if_true,
            6: self.jump_if_false,
            7: self.less_than,
            8: self.equals,
            99: self.halt
        }

    def run_program(self):
        """Run the Intcode program and fill the output and result properties"""
        self.pos = 0  # static starting point - points to first opcode in the set
        self.output = ""  # start out with empty output
        print('\t\t. . . . . StArTiNg PrOgRaM . . . . .')
        while self.pos < len(self.instruction_set):
            try:
                if self.instruction_set[self.pos] > 99:
                    # OpCode is "moded" - last 2 digits are the code, previous (right-to-left) indicate modi
                    modes = self.instruction_set[self.pos] // 100
                    opcode = self.instruction_set[self.pos] % 100 if self.instruction_set[self.pos] <= 999 \
                        else self.instruction_set[self.pos] % 1000 % 100
                    mode_0 = modes % 10
                    mode_1 = modes // 10
                else:
                    # Default modi
                    opcode = self.instruction_set[self.pos]
                    mode_0 = 0
                    mode_1 = 0

                kwargs = {
                    'set': self.instruction_set,
                    'mode_0': mode_0,
                    'mode_1': mode_1
                }

                self.opcodes[opcode](**kwargs)  # Run code through program (first part of tuple in opcodes dict)

            except ForceHalt:
                # Triggers on OpCode 99
                break

    def add(self, **kwargs):
        # Define for readability/clarity what kwargs are expected
        codes = kwargs['set']
        mode_0 = kwargs['mode_0']
        mode_1 = kwargs['mode_1']
        val_0 = codes[codes[self.pos + 1]] if mode_0 == 0 else codes[self.pos + 1]
        val_1 = codes[codes[self.pos + 2]] if mode_1 == 0 else codes[self.pos + 2]
        codes[codes[self.pos + 3]] = val_0 + val_1
        # Increment by length of code + parameters
        self.pos += 4

    def multiply(self, **kwargs):
        # Define for readability/clarity what kwargs are expected
        codes = kwargs['set']
        mode_0 = kwargs['mode_0']
        mode_1 = kwargs['mode_1']
        val_0 = codes[codes[self.pos + 1]] if mode_0 == 0 else codes[self.pos + 1]
        val_1 = codes[codes[self.pos + 2]] if mode_1 == 0 else codes[self.pos + 2]
        codes[codes[self.pos + 3]] = val_0 * val_1
        # Increment by length of code + parameters
        self.pos += 4

    def get_input(self, **kwargs):
        codes = kwargs['set']
        mode_0 = kwargs['mode_0']
        user_input = int(input('PlEaSe PrOvIdE DeViCe IdEnTiFiCaTiOn . . :  '))
        if mode_0 == 0:
            codes[codes[self.pos + 1]] = user_input
        elif mode_0 == 1:
            codes[self.pos + 1] = user_input
        # Increment by length of code + parameters
        self.pos += 2

    def put_output(self, **kwargs):
        codes = kwargs['set']
        mode_0 = kwargs['mode_0']
        if mode_0 == 0:
            self.output += str(codes[codes[self.pos + 1]])
        elif mode_0 == 1:
            self.output += str(codes[self.pos + 1])
        # Increment by length of code + parameters
        self.pos += 2

    def jump_if_true(self, **kwargs):
        codes = kwargs['set']
        mode_0 = kwargs['mode_0']
        mode_1 = kwargs['mode_1']
        compare_with = codes[codes[self.pos + 1]] if mode_0 == 0 else codes[self.pos + 1]
        if compare_with != 0:
            # Jump confirmed - check mode and go
            if mode_1 == 0:
                self.pos = codes[codes[self.pos + 2]]
            elif mode_1 == 1:
                self.pos = codes[self.pos + 2]
        else:
            # Pass on by
            self.pos += 3

    def jump_if_false(self, **kwargs):
        codes = kwargs['set']
        mode_0 = kwargs['mode_0']
        mode_1 = kwargs['mode_1']
        compare_with = codes[codes[self.pos + 1]] if mode_0 == 0 else codes[self.pos + 1]
        if compare_with == 0:
            # Jump confirmed - check mode and go
            if mode_1 == 0:
                self.pos = codes[codes[self.pos + 2]]
            elif mode_1 == 1:
                self.pos = codes[self.pos + 2]
        else:
            # Pass on by
            self.pos += 3

    def less_than(self, **kwargs):
        codes = kwargs['set']
        mode_0 = kwargs['mode_0']
        mode_1 = kwargs['mode_1']

        val_0 = codes[codes[self.pos + 1]] if mode_0 == 0 else codes[self.pos + 1]
        val_1 = codes[codes[self.pos + 2]] if mode_1 == 0 else codes[self.pos + 2]

        codes[codes[self.pos + 3]] = 1 if val_0 < val_1 else 0
        # Increment by length of code + parameters
        self.pos += 4

    def equals(self, **kwargs):
        codes = kwargs['set']
        mode_0 = kwargs['mode_0']
        mode_1 = kwargs['mode_1']

        val_0 = codes[codes[self.pos + 1]] if mode_0 == 0 else codes[self.pos + 1]
        val_1 = codes[codes[self.pos + 2]] if mode_1 == 0 else codes[self.pos + 2]

        codes[codes[self.pos + 3]] = 1 if val_0 == val_1 else 0
        # Increment by length of code + parameters
        self.pos += 4

    @staticmethod
    def halt(**kwargs):
        # Argument acception required - otherwise things go tits up
        raise ForceHalt


if __name__ == "__main__":
    print('~*-_= ThErMaL EnViRoNmEnT SuPeRvIsIoN TeRmInAl =_-*~')
    raw_input = open('input.txt', 'r').read().split(',')

    # Process the input - all values are to be ints (not strings)
    #   Note: map(x, y) executes function x on each element in iterable y and returns an iterable map object
    #   Conversion from map to list is done mostly to use list's added functions
    program = list(map(int, raw_input))

    print('\tInItIaLiZiNg PhAsE 1 . . .')
    computer_part1 = Intcode(program.copy())
    computer_part1.run_program()
    print(f'. . . FiNiShEd PrOgRaM: CoOlInG . . . \n\tDiAgNoStIc CoDe : {computer_part1.output.replace("0", "")} . . .')

    print('\tInItIaLiZiNg PhAsE 2 . . .')
    computer_part2 = Intcode(program.copy())
    computer_part2.run_program()
    print(f'. . . FiNiShEd PrOgRaM: HeAtInG . . .\n\tDiAgNoStIc CoDe : {computer_part2.output} . . .')
