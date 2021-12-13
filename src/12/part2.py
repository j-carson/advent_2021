from collections import Counter, defaultdict, namedtuple
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


TEST_2A_SOLUTION = 36
TEST_2B_SOLUTION = 103
TEST_2C_SOLUTION = 3509


class Graph:
    def __init__(self, data):
        self.connects_to = defaultdict(set)
        for line in data:
            ptA, ptB = line
            # The "next point from here" should never be "back to start"
            # The "next point from here" should be nowhere if we are at the end
            if ptA != "start" and ptB != "end":
                self.connects_to[ptB].add(ptA)
            if ptB != "start" and ptA != "end":
                self.connects_to[ptA].add(ptB)

        ic(self.connects_to)

    def take_step(self, path):
        """add one step to path, if possible or stop iteration"""

        possible_steps = self.connects_to[path[-1]]

        for step in possible_steps:
            if step.islower():
                count_small_visits = Counter([p for p in path if p.islower()])
                used_revisit = 2 in count_small_visits.values()

                if (count_small_visits[step] == 1 and used_revisit) or (
                    count_small_visits[step] == 2
                ):
                    # skip this one - breaks the rules
                    continue

            yield path + [step]

    def make_paths(self, path):
        for option in self.take_step(path):
            if option[-1] == "end":
                yield option
            else:
                yield from self.make_paths(option)

    def make_all_paths(self):
        path = ["start"]

        i = -1
        for i, new_path in enumerate(self.make_paths(path)):
            if i < 50:
                ic(i, new_path)
        return i + 1


def solve2(data):
    cavemap = Graph(data)
    score = cavemap.make_all_paths()
    ic(score)
    return score


def parsetext(text):
    lines = text.splitlines()

    return [line.split("-") for line in lines]


def mydata():
    return Path("input.txt").read_text()


def part2():

    # turn on debug print statements
    ic.enabled = False
    result = solve2(parsetext(TEST_INPUT_1A))
    assert result == TEST_2A_SOLUTION

    result = solve2(parsetext(TEST_INPUT_1B))
    assert result == TEST_2B_SOLUTION

    result = solve2(parsetext(TEST_INPUT_1C))
    assert result == TEST_2C_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return solve2(parsetext(mydata()))


result = part2()
print("Part 2: ", result)
