import ast
import re
from itertools import product
from pathlib import Path

from tqdm import tqdm
from ycecream import y as ic

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
    __slots__ = ["registers"]

    def __init__(self):
        self.registers = {key: key for key in "wxyz"}

    def reset(self):
        self.__init__()

    def __getitem__(self, key):
        return self.registers[key]

    def __setitem__(self, key, value):
        self.registers[key] = value

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
            self[dest] = f"int({arg1} == {arg2})"

    @staticmethod
    def cheatcodes(code, index):
        """More hand-optimizations"""

        # z % 26 is between 0 and 25 for any z, input digits are between 1 and 9
        # if you add a number greater than 10 to the result of the mod, you
        # can't be equal to an input
        code = code.replace(
            "((25 * int(int(((z % 26) + 10) == INPUT) == 0)) + 1)", "26"
        )
        code = code.replace(
            "((25 * int(int(((z % 26) + 11) == INPUT) == 0)) + 1)", "26"
        )
        code = code.replace(
            "((25 * int(int(((z % 26) + 12) == INPUT) == 0)) + 1)", "26"
        )
        code = code.replace(
            "((25 * int(int(((z % 26) + 14) == INPUT) == 0)) + 1)", "26"
        )

        code = code.replace("int(int(((z % 26) + 10) == INPUT) == 0)", "1")
        code = code.replace("int(int(((z % 26) + 11) == INPUT) == 0)", "1")
        code = code.replace("int(int(((z % 26) + 12) == INPUT) == 0)", "1")
        code = code.replace("int(int(((z % 26) + 14) == INPUT) == 0)", "1")

        # generically, int(int((expression) == INPUT) == 0)
        # simplifies to int((expression) != INPUT)
        pattern = re.compile(r"int\(int\(\(.+?\) == INPUT\) == 0\)")
        newcode = code
        for match in pattern.finditer(code):
            original = match.group()
            replacement = original.replace("int(int(", "int(")
            replacement = replacement.replace("== INPUT) == 0)", "!= INPUT)")
            newcode = newcode.replace(original, replacement)
            ic(original, replacement)

        if code != newcode:
            # ic(code, newcode)
            code = newcode

        # generically, ((expression) * 1), simplifies to (expression)
        pattern = re.compile(r"\(\([^(]+?\) \* 1\)")
        newcode = code
        for match in pattern.finditer(code):
            original = match.group()
            replacement = original[1:].replace(" * 1)", "")
            newcode = newcode.replace(original, replacement)
            ic(original, replacement)

        if code != newcode:
            # ic(code, newcode)
            code = newcode

        code = code.replace("INPUT", f"INPUTS[{index}]")

        # Now for the truly ugly stuff...
        # z = ((z * 26) + (expression)) rewrites to PUSH expression
        push = "((z * 26) + ("
        if code.startswith(push):
            code = code[:-2].replace(push, "")
            return "PUSH " + code

        # OK, it's not a push, must be a pop
        pattern = re.compile(r"int\(\(\([^)]+?\)[^)]+?\)[^)]+?\)")
        match = pattern.search(code)
        expression = match.group()[4:-1].replace("(z % 26)", "STACK")
        return expression

    def run(self, program):
        """The input consists of 14 sequences of 17 mostly-the-same instructions.
        Only "z" and INPUT matter in each chunk (by hand-analysis of input because
        this puzzle is awful)"""
        stored_procedures = {}

        for chunk in range(14):
            subroutine = program[chunk * 18 : (chunk + 1) * 18]
            for line in subroutine:
                opcode, *args = line.split()
                if opcode == "inp":
                    dest = args[0]
                    self[dest] = f"INPUT"
                else:
                    opfunc = getattr(self, opcode)
                    dest, arg2 = args
                    arg1 = self[dest]
                    if arg2 in "wxyz":
                        arg2 = self[arg2]
                    opfunc(dest, arg1, arg2)

            procname = f"func{chunk}"
            stored_procedures[procname] = self.cheatcodes(self["z"], chunk)
            self.reset()

        return stored_procedures


ic.enabled = False
alu = ALU()
code = alu.run(DATA)

output = Path("output_opt.py").open("w")

output.write("def eval_license(INPUTS):\n")

stack = []
for i in range(14):
    funcname = f"func{i}"
    expression = code[funcname]
    if expression.startswith("PUSH"):
        expression = expression[5:]
        stack = stack + [expression]
    else:
        expression = expression.replace("STACK", stack.pop())
        output.write(f"    if {expression}: return False\n")

output.write("    return True\n")
output.close()
