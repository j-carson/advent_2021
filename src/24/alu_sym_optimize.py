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


stored_procedures = {}
procedure_names = {}
func_ids = {}


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

    def run(self, program):
        """The input consists of 14 sequences of 17 instructions.
        Four the same, two different, eight the same, one different, two the same
        """

        result = []
        procedure_counter = 0

        for chunk in range(14):
            subroutine = program[chunk * 18 : (chunk + 1) * 18]

            sub1 = subroutine[0:15]
            sub2 = subroutine[15:]

            result.append("INPUT")
            for subpart in (sub1, sub2):
                chunkname = "\n".join(subpart)
                if chunkname not in stored_procedures:
                    for line in subpart:
                        opcode, *args = line.split()
                        if opcode == "inp":
                            dest = args[0]
                            self[dest] = "INPUT"
                        else:
                            opfunc = getattr(self, opcode)
                            dest, arg2 = args
                            arg1 = self[dest]
                            if arg2 in "wxyz":
                                arg2 = self[arg2]
                            opfunc(dest, arg1, arg2)

                    code = dict(w=self["w"], x=self["x"], y=self["y"], z=self["z"])
                    stored_procedures[chunkname] = code

                    procname = f"func{procedure_counter}"
                    procedure_counter += 1
                    procedure_names[chunkname] = procname
                    func_ids[procname] = chunkname

                func_id = procedure_names[chunkname]
                result.append(func_id)
                # pop off the input we just read
                self.reset()
        return result


alu = ALU()
code = alu.run(DATA)

output = Path("output_opt.py").open("w")
output.write("from functools import cache\n")

args = {}
returns = {}
for func_name, source in func_ids.items():
    # figure out which registers change and make those
    # return values
    registers = stored_procedures[source]
    return_vals = [key for key, val in registers.items() if key != val]
    returns[func_name] = return_vals
    proc = ",".join([registers[reg] for reg in return_vals])

    # figure out which registers are in expressions and
    # make those arguments
    arglist = []
    for arg in ("w", "x", "y", "z", "INPUT"):
        if arg in proc:
            arglist.append(arg)
    args[func_name] = arglist
    argdecl = ",".join(arglist)

    output.write(f"@cache\n")
    output.write(f"def {func_name}({argdecl}):\n")
    output.write(f"    return {proc}\n")

output.write("def eval_license(INPUTS):\n")
output.write("    w = x = y = z = 0\n")

input_counter = 0

for line in code:
    if line == "INPUT":
        output.write(f"    INPUT = INPUTS[{input_counter}]\n")
        input_counter += 1
    else:
        argdecl = ",".join(args[line])
        retdecl = ",".join(returns[line])
        output.write(f"    {retdecl} = {line}({argdecl})\n")

output.write("    return (z == 0)\n")
output.close()
