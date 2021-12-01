# Template

from pathlib import Path

import pandas as pd


def inputparser():
    return pd.read_csv("input.txt", header=None)[0]


def part1():
    data = inputparser()
    return (data.diff() > 0).sum()


def part2():
    data = inputparser()
    sums = data.rolling(3).sum()
    return (sums.diff() > 0).sum()


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
