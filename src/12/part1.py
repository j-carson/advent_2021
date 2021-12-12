from collections import defaultdict, namedtuple
from pathlib import Path

import numpy as np
import pandas as pd
from ycecream import y as ic

TEST_INPUT_1A = """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
TEST_INPUT_1B = """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc"""
TEST_INPUT_1C = """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW"""


TEST_1A_SOLUTION = 10
TEST_1B_SOLUTION = 19
TEST_1C_SOLUTION = 226


class Graph:
    def __init__(self, data):
        tokens = []
        for line in data:
            tokens.extend(line)
        tokens = np.unique(tokens)
        df = pd.DataFrame(index=tokens, columns=tokens, dtype=bool, data=False)
        for line in data:
            ptA, ptB = line
            df.loc[ptA, ptB] = df.loc[ptB, ptA] = True

        self.connects_to = defaultdict(list)
        for token in tokens:
            for next_dest in tokens:
                if df.loc[token, next_dest]:
                    self.connects_to[token].append(next_dest)
        ic(self.connects_to)

    def take_step(self, path):
        """add one step to path, or return None if no valid step exists"""
        possible_steps = self.connects_to[path[-1]]
        for step in possible_steps:
            if (step.lower() == step) and step in path:
                continue
            yield path.copy() + [step]

    def make_paths(self, path):
        for option in self.take_step(path):
            if option[-1] == "end":
                yield path
            else:
                yield from self.make_paths(option)

    def make_all_paths(self):
        path = ["start"]
        for i, new_path in enumerate(self.make_paths(path)):
            ic(i, new_path)
        return i + 1


def solve1(data):
    cavemap = Graph(data)
    score = cavemap.make_all_paths()
    return score


def solve2(data):
    return 0


def parsetext(text):
    lines = text.splitlines()

    return [line.split("-") for line in lines]


def mydata():
    return Path("input.txt").read_text()


def part1():
    # turn on debug print statements
    ic.enabled = True
    result = solve1(parsetext(TEST_INPUT_1A))
    assert result == TEST_1A_SOLUTION

    result = solve1(parsetext(TEST_INPUT_1B))
    assert result == TEST_1B_SOLUTION

    result = solve1(parsetext(TEST_INPUT_1C))
    assert result == TEST_1C_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return solve1(parsetext(mydata()))


result = part1()
print("Part 1: ", result)
