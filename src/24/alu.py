from itertools import product
from pathlib import Path

DEBUG = False
DATA = Path("input.txt").read_text().splitlines()


class ALU:
    __slots__ = ["registers"]

    def __init__(self):
        self.registers = {key: 0 for key in "wxyz"}

    def __getitem__(self, key):
        return self.registers[key]

    def __setitem__(self, key, value):
        self.registers[key] = value

    def trace(self, line):
        if DEBUG:
            print(line, "\n", self.registers)

    def do_math(self, *args, mathfunc):
        # first operand to a mathematical operation is the destination
        # register, second operand can be another register or an int
        register, arg = args
        if arg in "wxyz":
            arg = self[arg]
        else:
            arg = int(arg)
        self[register] = mathfunc(self[register], arg)

    def mul(self, *args):
        self.do_math(*args, mathfunc=lambda a, b: a * b)

    def add(self, *args):
        self.do_math(*args, mathfunc=lambda a, b: a + b)

    def div(self, *args):
        self.do_math(*args, mathfunc=lambda a, b: a // b)

    def mod(self, *args):
        self.do_math(*args, mathfunc=lambda a, b: a % b)

    def eql(self, *args):
        self.do_math(*args, mathfunc=lambda a, b: int(a == b))

    def run(self, inputs, program):
        for line in program:
            opcode, *args = line.split()
            if opcode == "inp":
                line += f" from {inputs}"
                dest = args[0]
                self[dest] = inputs[0]
                inputs = inputs[1:]
            else:
                opfunc = getattr(self, opcode)
                opfunc(*args)
            self.trace(line)
        return self["z"] == 0


alu = ALU()
for i, inputs in enumerate(product(range(9, 0, -1), repeat=14)):
    if alu.run(inputs, DATA):
        print(inputs)
        break
    if i % 500 == 0:
        print(".", end="")
