from intcode import Intcode as Computer


# Source: https://www.w3resource.com/python-exercises/basic/python-basic-1-exercise-12.php
# Recursive permutations-builder, I thought of this but they made it 'for me'!
def permute(nums):
    result_perms = [[]]
    for n in nums:
        new_perms = []
        for perm in result_perms:
            for i in range(len(perm)+1):
                new_perms.append(perm[:i] + [n] + perm[i:])
                result_perms = new_perms
    return result_perms


def amplifier(i_set, inputs):
    amp = Computer(i_set, amp_inputs=inputs)
    amp.run_program()
    return int(amp.output)


def amp_to_thruster(phase_set, i_set):
    # Handles amp chaining, returns [signal, [phase_order]]
    resultant_set = [0, []]
    possible_phases = permute(phase_set)

    for phases in possible_phases:
        amps = []
        temp_result = 0
        halted = False
        for phase in phases:
            temp_amp = Computer(i_set.copy(), amp_inputs=[phase, temp_result], pause_on_output=True)
            temp_amp.run_program()
            temp_result = int(temp_amp.output)
            amps.append(temp_amp)

        i = 0

        while not halted:
            amps[i].run_program(amp_inputs=[temp_result])
            halted = amps[i].halted
            if not halted:
                # print(f'amp output: {amps[i].output} - halted? {amps[i].halted}')
                temp_result = int(amps[i].output)
                i += 1
                if i == len(amps):
                    i = 0  # Reset and loop
            # print(f'halted? {halted}')

        if temp_result > resultant_set[0]:
            # print(f'New record: {temp_result} using set {phases}')
            resultant_set = [temp_result, phases]

    return resultant_set


if __name__ == "__main__":
    raw_input = open('input.txt', 'r').read().split(',')
    # Process the input - all values are to be ints (not strings)
    #   Note: map(x, y) executes function x on each element in iterable y and returns an iterable map object
    #   Conversion from map to list is done mostly to use list's added functions
    program = list(map(int, raw_input))

    # Intcode was altered to allow for inputs to be preset
    state_set = [0, 1, 2, 3, 4]     # possible states
    possible_states = permute(state_set)
    max_result = [0, []]

    for states in possible_states:
        result = 0      # Initial result/input
        for state in states:
            result = amplifier(program.copy(), [state, result])
        if result > max_result[0]:
            max_result = [result, states]

    print(f'\t-- Part 1 --\n\t\tMax output is {max_result[0]} using series {max_result[1]}')

    possible_states = [5, 6, 7, 8, 9]
    max_result = amp_to_thruster(possible_states, program.copy())
    print(f'\t-- Part 2 --\n\t\tMax output is {max_result[0]} using series {max_result[1]}')
