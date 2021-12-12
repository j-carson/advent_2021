# thinking about a "no bad options on the map" version of the algorithm
# to see if that makes the if-tests less hairy
from collections import Counter, defaultdict, namedtuple
from itertools import count
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


class CaveMap:
    def __init__(self):
        # connects_do is a dictionary:
        # key = location, value = valid next steps
        self.connects_to = defaultdict(set)

    def clone(self):
        result = CaveMap()
        for token, connections in self.connects_to.items():
            result.connects_to[token] = connections.copy()
        return result

    def load_data(self, data):
        for line in data:
            ptA, ptB = line
            # The "next point from here" should never be "back to start"
            # The "next point from here" should be nowhere if we are at the end
            if ptA != "start" and ptB != "end":
                self.connects_to[ptB].add(ptA)
            if ptB != "start" and ptA != "end":
                self.connects_to[ptA].add(ptB)
        ic(self.connects_to)
        return self

    def remove_destination(self, no_revisit):
        old_map = self.connects_to
        self.connects_to = defaultdict(set)

        for token, connections in old_map.items():
            if no_revisit in connections:
                self.connects_to[token] = set(
                    [item for item in connections if item != no_revisit]
                )
            else:
                self.connects_to[token] = connections
        return self


class CavePath:
    def __init__(self, cavemap, path=["start"]):
        self.tokens = path
        self.cavemap = cavemap

    def take_step(self):
        """add one step to path, if possible or stop iteration"""

        possible_steps = self.cavemap.connects_to[self.tokens[-1]]

        for step in possible_steps:
            if step.islower():
                count_small_visits = Counter([t for t in self.tokens if t.islower()])
                used_revisit = 2 in count_small_visits.values()

                if count_small_visits[step] == 0:
                    if used_revisit:
                        # if we've used the revisit option, we can't come back here
                        yield CavePath(
                            self.cavemap.clone().remove_destination(step),
                            self.tokens + [step],
                        )
                    else:
                        # revisiting here is still an option
                        yield CavePath(self.cavemap, self.tokens + [step])

                elif count_small_visits[step] == 1:
                    assert not used_revisit

                    # we need to remove all the current visits to small caves
                    # from the map as we are using up the single revisit option
                    newmap = self.cavemap.clone()
                    for token in count_small_visits.keys():
                        newmap = newmap.remove_destination(token)

                    yield CavePath(newmap, self.tokens + [step])
                else:
                    assert (
                        False
                    ), f"Unexpected count_small_visits[{step}] == {count_small_visits[step]}"

            else:
                yield CavePath(self.cavemap, self.tokens + [step])

    def make_paths(self):
        for option in self.take_step():
            if option.tokens[-1] == "end":
                yield option
            else:
                yield from option.make_paths()


def solve2(data):
    cavemap = CaveMap().load_data(data)
    for score, path in zip(count(1), CavePath(cavemap).make_paths()):
        if score < 20:
            # preint out a few examples for debugging
            ic(path.tokens)

    ic(score)
    return score


def parsetext(text):
    lines = text.splitlines()

    return [line.split("-") for line in lines]


def mydata():
    return Path("input.txt").read_text()


def part2():

    # turn on debug print statements
    ic.enabled = True
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
