from pathlib import Path

import numpy as np
from ycecream import y as ic

TEST_INPUT = "test_input"
TEST_1_SOLUTION = 0
TEST_2_SOLUTION = 0


def solve1(data):
    return 0


def solve2(data):
    return 0


def parsetext(text):
    lines = text.splitlines()
    return ic(lines)


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
