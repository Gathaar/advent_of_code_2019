from typing import List


class Intcode:
    def __init__(self, program: List[int]):
        self.pos = 0
        self.initial_state = program.copy()    # for debug/test
        self.program = program
        self.output = ''
        self.ran_fully = False

    def run_code(self):
        opcodes = {
            1:  self.add,
            2:  self.multiply,
            99:  self.end
        }
        routine = opcodes.get(self.program[self.pos])
        if routine:
            routine()
        else:
            self.end()

# region opcodes
    def add(self):
        # Get positions
        first_position = self.program[self.pos + 1]
        second_position = self.program[self.pos + 2]
        third_position = self.program[self.pos + 3]
        # Get data
        first_number = self.program[first_position]
        second_number = self.program[second_position]
        self.program[third_position] = first_number + second_number
        self.pos += 4

    def multiply(self):
        # Get positions
        first_position = self.program[self.pos + 1]
        second_position = self.program[self.pos + 2]
        third_position = self.program[self.pos + 3]
        # Get data
        first_number = self.program[first_position]
        second_number = self.program[second_position]
        self.program[third_position] = first_number * second_number
        self.pos += 4

    def end(self):
        self.ran_fully = True
# endregion

    def get_part_1_output(self):
        return self.program[0]

    def run(self):
        self.ran_fully = False
        while not self.ran_fully:
            self.run_code()

    def __str__(self):
        # Returns list of ints, not very stringy
        return self.program


def part2(program, desired_result) -> int:
    coder = Intcode(program)
    lo = 0
    hi = 99
    noun = lo
    while noun <= hi:
        verb = lo
        while verb <= hi:
            # Reset and prep
            coder.program = coder.initial_state.copy()
            coder.pos = 0
            coder.program[1] = noun
            coder.program[2] = verb
            coder.run()
            print(f'Ran with noun = {noun} and verb = {verb} -- output {coder.get_part_1_output()} and coder pos {coder.pos}')
            if coder.get_part_1_output() == desired_result:
                return 100 * noun + verb
            verb += 1
        noun += 1
    return -1


if __name__ == '__main__':
    input_program_raw = open('input.txt').read().split(',')
    input_program = []
    for command in input_program_raw:
        input_program.append(int(command))
    computer = Intcode(input_program.copy())
    # Damaged computer repairs
    computer.program[1] = 12
    computer.program[2] = 2
    computer.run()
    print(f'Day 2 Part 1 output: {computer.get_part_1_output()}')
    print(f'Day 2 Part 2 output: {part2(input_program, 19690720)}')


