from pathlib import Path

import numpy as np
from ycecream import y as ic

TEST_INPUT = "16,1,2,0,4,2,7,1,2,14"
TEST_1_SOLUTION = 37
TEST_2_SOLUTION = 168


def solve1(crabs, counts):
    # The best spot will be somewhere between the lowest and
    # highest location, and we'll know we crossed the minimum
    # when we stop getting lower scores
    low = crabs[0]
    high = crabs[-1]
    best = np.abs(crabs - low).sum()

    for pos in range(low + 1, high):
        score = (np.abs(crabs - pos) * counts).sum()
        if score < best:
            best = score
        else:
            break

    return best


def score2(crabs, counts, location):
    # formula for sum of series of integers
    # is the average of the endpoints times
    # the total number of items in the series
    distances = np.abs(crabs - location)
    costs = (distances + 1) * distances / 2
    return (costs * counts).sum()


def solve2(crabs, counts):
    low = crabs[0]
    high = crabs[-1]

    best = score2(crabs, counts, low)

    for pos in range(low + 1, high):
        score = score2(crabs, counts, pos)
        if score < best:
            best = score
        else:
            break

    return int(best)


def parsetext(text):
    return np.unique([int(i) for i in text.split(",")], return_counts=True)


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


def part2():

    # turn on debug print statements
    ic.enabled = True
    result = solve2(*parsetext(TEST_INPUT))
    assert result == TEST_2_SOLUTION

    # turn off debug print statements
    ic.enabled = True
    return solve2(*parsetext(mydata()))


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
