from collections import Counter
from functools import lru_cache
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


RULES = {}


def score(tally):
    count_values = list(tally.values())
    return max(count_values) - min(count_values)


def combine_tallys(tally1, tally2, de_dup):
    tally = tally1.copy()
    for key in tally2:
        tally[key] += tally2[key]
    tally[de_dup] -= 1
    return tally


@lru_cache(maxsize=10_000)
def tally_polymer(polymer, nsteps):

    assert nsteps >= 0
    assert len(polymer) >= 2

    if nsteps == 0:
        return Counter(polymer)

    elif len(polymer) > 2:
        tally1 = tally_polymer(polymer[:2], nsteps)
        tally2 = tally_polymer(polymer[1:], nsteps)
        return combine_tallys(tally1, tally2, polymer[1])

    elif polymer in RULES:
        return tally_polymer(polymer[0] + RULES[polymer] + polymer[1], nsteps - 1)

    else:
        return Counter(polymer)


def solve1(polymer, nsteps=10):
    result = score(tally_polymer(polymer, nsteps))
    tally_polymer.cache_clear()
    return result


def solve2(polymer):
    return solve1(polymer, 40)


def parsetext(text):

    chunks = text.split("\n\n")
    template = chunks[0]

    lines = chunks[1].splitlines()
    RULES.clear()
    for line in lines:
        parts = line.split(" -> ")
        RULES[parts[0]] = parts[1]

    return template


def mydata():
    return Path("input.txt").read_text()


def part1():
    # turn on debug print statements
    ic.enabled = True
    polymer = parsetext(TEST_INPUT)
    result = solve1(polymer)
    assert result == TEST_1_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    polymer = parsetext(mydata())
    result = solve1(polymer)
    assert result == 3411
    return result


def part2():
    # turn off debug print statements
    ic.enabled = False
    return solve2(parsetext(mydata()))


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
