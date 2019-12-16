# Custom exception to halt without extra trouble
class ForceHalt(Exception):
    pass


class ForcePause(Exception):
    pass


# noinspection SpellCheckingInspection
class Intcode:
    pos = None
    output = None
    amp_inputs = []
    pause_on_output = False
    halted = False

    def __init__(self, instruction_set, **kwargs):
        # Assume the instruction_set is a list (or at least iterable) of ints
        # print(f'\t. . . InItIaLiZiNg . . .')
        self.instruction_set = instruction_set
        self.pos = 0  # static starting point - points to first opcode in the set
        self.output = ""  # start out with empty output
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
        self.__dict__.update(kwargs)    # sets properties by using kwargs

    def run_program(self, **kwargs):
        """Run the Intcode program and fill the output and result properties"""
        # print('\t\t. . . . . StArTiNg PrOgRaM . . . . .')
        self.output = ""    # Reset
        if self.halted:
            print('Attempting to run when halted - no can do!')
            return  # Possibly make this a raise instead?

        # Add kwargs to manipulate the program (if required)
        self.__dict__.update(kwargs)
        # print(f'Output reached! currently using inputs: {self.amp_inputs}')

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

            except ForcePause:
                # Triggers on "user" demanding a stop to continue
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

        if self.amp_inputs:
            user_input = self.amp_inputs.pop(0)
        else:
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
        if self.pause_on_output:
            raise ForcePause

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

    def halt(self, **kwargs):
        # Argument acception required - otherwise things go tits up
        self.halted = True
        raise ForceHalt
