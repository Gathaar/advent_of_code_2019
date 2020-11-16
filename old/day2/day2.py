import unittest


class Testing(unittest.TestCase):
    def test_part1(self):
        test = [[[1, 0, 0, 0, 99], [2, 0, 0, 0, 99]],
                [[2, 3, 0, 3, 99], [2, 3, 0, 6, 99]],
                [[2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]],
                [[1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99]]]
        for case in test:
            self.assertEqual(case[1], day2pt1(case[0]))


def day2pt1(program):
    pos = 0  # initial position
    while True:
        code = program[pos]
        # print(f'Handling code {code} at position {pos}')
        if code == 1:  # 1: ADD pos+1 and pos+2 elements, store in pos[pos+3]
            input1_pos = program[pos + 1]
            input2_pos = program[pos + 2]
            output_pos = program[pos + 3]
            program[output_pos] = program[input1_pos] + program[input2_pos]
        elif code == 2:  # 2: MULTIPLY (rest same as 1)
            input1_pos = program[pos + 1]
            input2_pos = program[pos + 2]
            output_pos = program[pos + 3]
            program[output_pos] = program[input1_pos] * program[input2_pos]
        elif code == 99:  # ABORT
            return program
        else:
            print(f'Found {code} and didn\'t know what to do with it - aborting!')
            return program
        # "Jump" to next opcode
        pos += 4


def day2pt2(program, desired_output):
    # program[1] and program[2] can be changed, rest CANNOT
    for i in range(100):
        for j in range(100):
            attempt = program.copy()
            attempt[1] = i
            attempt[2] = j
            if day2pt1(attempt)[0] == desired_output:
                # format output
                output = ""
                if i > 9:
                    output += str(i)
                else:
                    output += "0" + str(i)

                if j > 9:
                    output += str(j)
                else:
                    output += "0" + str(j)

                return output
    # Uh oh, Santa's helper sucks!
    return "xxxx"


if __name__ == "__main__":
    # Reads, then splits on "," to make an array of OpCodes
    raw_puzzle_input = open("input.txt", 'r').read().split(',')

    puzzle_input = []   # clean the mess
    for inp in raw_puzzle_input:
        puzzle_input.append(int(inp))

    # Prep for reboot... (part 1)
    part1_puzzle_input = puzzle_input.copy()
    part1_puzzle_input[1] = 12
    part1_puzzle_input[2] = 2
    print(f'Solution for day 2 part 1: {day2pt1(part1_puzzle_input)[0]}')

    # Prepping for gravity assist... (part 2)
    # Output required: 19690720
    print(f'Solution for day 2 part 2: {day2pt2(puzzle_input, 19690720)}')
