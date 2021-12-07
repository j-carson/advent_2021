from pathlib import Path

import numpy as np
from ycecream import y as ic

TEST_INPUT = "16,1,2,0,4,2,7,1,2,14"
TEST_1_SOLUTION = 37
TEST_2_SOLUTION = 168


def solve1(data):
    data = np.array(sorted(data), dtype=int)

    best = np.abs(data - data[0]).sum()

    for pos in data:
        score = np.abs(data - pos).sum()
        if score < best:
            best = score

    return best


def score2(crabs, location):
    distances = np.abs(crabs - location)
    costs = (distances + 1) * distances / 2
    return costs.sum()


def solve2(data):
    data = np.array(sorted(data), dtype=int)
    low = data[0]
    high = data[-1]

    best = score2(data, data[0])

    for pos in range(low + 1, high):
        score = score2(data, pos)
        if score < best:
            best = score

    return best


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
    ic.enabled = True
    return solve2(parsetext(mydata()))


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
