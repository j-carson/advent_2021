import ast
from itertools import product
from pathlib import Path

from tqdm import tqdm

DEBUG = False
DATA = Path("input.txt").read_text().splitlines()


def isint(thing):
    try:
        value = int(thing)
        return True
    except ValueError:
        pass
    return False


class ALU:
    __slots__ = ["registers", "expressions_set", "expressions_ordering"]

    def __init__(self):
        self.expressions_set = set()
        self.expressions_ordering = []
        self.registers = {key: "0" for key in "wxyz"}

    def __getitem__(self, key):
        return self.registers[key]

    def __setitem__(self, key, value):

        if "INPUT" not in value:
            value = str(eval(value))

        if value.startswith("(") and (value not in self.expressions_set):
            self.expressions_set.add(value)
            self.expressions_ordering.append(value)

        self.registers[key] = value

    def trace(self, line):
        if DEBUG:
            print(line, "\n", self.registers)

    def mul(self, dest, arg1, arg2):
        if arg1 == "0" or arg2 == "0":
            self[dest] = "0"
        elif arg1 == "1":
            self[dest] = arg2
        elif arg2 == "1":
            self[dest] = arg1
        else:
            self[dest] = f"({arg1} * {arg2})"

    def add(self, dest, arg1, arg2):
        if arg1 == "0":
            self[dest] = arg2
        elif arg2 == "0":
            self[dest] = arg1
        else:
            self[dest] = f"({arg1} + {arg2})"

    def div(self, dest, arg1, arg2):
        if arg2 == "1":
            self[dest] = arg1
        else:
            self[dest] = f"({arg1} // {arg2})"

    def mod(self, dest, arg1, arg2):
        self[dest] = f"({arg1} % {arg2})"

    def eql(self, dest, arg1, arg2):
        # if comparing an input and a constant, use
        # the fact that input is between 1 and 9
        if isint(arg1) and arg2.startswith("INPUT"):
            val = int(arg1)
            if (val < 1) or (val > 9):
                self[dest] = "0"
                return
        elif isint(arg2) and arg1.startswith("INPUT"):
            val = int(arg2)
            if (val < 1) or (val > 9):
                self[dest] = "0"
                return
        else:
            self[dest] = f"(int({arg1} == {arg2}))"

    def run(self, program):
        inputs_counter = 0
        for line in program:
            opcode, *args = line.split()
            if opcode == "inp":
                dest = args[0]
                self[dest] = f"INPUT[{inputs_counter}]"
                inputs_counter += 1
            else:
                opfunc = getattr(self, opcode)

                dest, arg2 = args
                arg1 = self[dest]
                if arg2 in "wxyz":
                    arg2 = self[arg2]

                opfunc(dest, arg1, arg2)
            self.trace(line)
        return self


alu = ALU()
alu.run(DATA)
registers = alu.registers
repeated_expressions = alu.expressions_ordering

out = Path("output.py").open("w")
reverse_lookup = {}
out.write("def eval_license(INPUT):\n")

for varname, idx_expression in zip(
    product("bcdefghjklmnopqrtuvwxyz", repeat=2), enumerate(repeated_expressions)
):

    varname = "".join(varname)
    idx, expr = idx_expression
    previous_expressions = reversed(repeated_expressions[:idx])

    reverse_lookup[expr] = varname
    new_expr = expr
    for prex in previous_expressions:
        new_expr = expr.replace(prex, reverse_lookup[prex])
        if new_expr != expr:
            expr = new_expr

    out.write(f"    {varname} = {expr[1:-1]}\n")

prex = registers["z"]
out.write(f"    z = {reverse_lookup[prex]}\n")
out.write(f"    return (z == 0)\n")

out.close()
