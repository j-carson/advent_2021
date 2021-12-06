# An alternate implementation, using recursion

from collections import Counter
from functools import lru_cache
from pathlib import Path

import numpy as np
from ycecream import y as ic

TEST_INPUT = "3,4,3,1,2"
TEST_1_SOLUTION = 5934
TEST_2_SOLUTION = 26984457539


@lru_cache(maxsize=1024)
def fish_gen(lifecycle, ticks):
    """given one fish at stage 'lifecycle', how many
    will we have in clock 'ticks' time?"""

    if ticks <= lifecycle:
        # this fish doesn't have time to reproduce
        # so one-fish stays one-fish
        return 1
    else:
        # calculate the progeny recursively
        ticks -= lifecycle + 1
        return fish_gen(6, ticks) + fish_gen(8, ticks)


def solve1(data, generations=80):

    fish_counts_by_age = Counter(data)
    fish_count = 0
    for lifecycle, numfish in fish_counts_by_age.items():
        fish_count += numfish * fish_gen(lifecycle, generations)
    return fish_count


def solve2(data, generations=256):
    return solve1(data, generations)


def parsetext(text):
    return [int(i) for i in text.split(",")]


def mydata():
    return Path("input.txt").read_text()


def part1():
    # turn on debug print statements
    ic.enabled = True
    result = solve1(parsetext(TEST_INPUT))
    assert result == TEST_1_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return solve1(parsetext(mydata()))


def part2():

    # turn on debug print statements
    ic.enabled = True
    result = solve2(parsetext(TEST_INPUT))
    assert result == TEST_2_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return solve2(parsetext(mydata()))


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
