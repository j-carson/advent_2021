from collections import namedtuple
from pathlib import Path

import numpy as np
from ycecream import y as ic

TEST_INPUT = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

TEST_1_SOLUTION = 1588
TEST_2_SOLUTION = 0


def yield_pairs(polymer):
    for tup in zip(polymer, polymer[1:]):
        yield "".join(tup)


def grow_polymer(polymer, rules):
    result = ""
    for char, pair in zip(polymer, yield_pairs(polymer)):
        result += char
        if pair in rules:
            result += rules[pair]
    result += polymer[-1]
    return result


def score1(polymer):
    values, counts = np.unique(list(polymer), return_counts=True)
    return np.max(counts) - np.min(counts)


def solve1(polymer, rules, nsteps=10):

    for i in range(nsteps):
        polymer = grow_polymer(polymer, rules)
    return score1(polymer)


def parsetext(text):
    chunks = text.split("\n\n")
    template = chunks[0]

    rules = {}
    lines = chunks[1].splitlines()
    for line in lines:
        parts = line.split(" -> ")
        rules[parts[0]] = parts[1]

    return template, rules


def mydata():
    return Path("input.txt").read_text()


def part1():
    # turn on debug print statements
    ic.enabled = True
    result = solve1(*parsetext(TEST_INPUT))
    assert result == TEST_1_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return solve1(*parsetext(mydata()))


result = part1()
print("Part 1: ", result)
