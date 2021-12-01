# Template

from pathlib import Path

import pandas as pd


def inputparser():
    text = Path("input.txt").read_text()
    lines = text.splitlines()
    return [int(l) for l in lines]


def part1():
    data = pd.Series(inputparser())
    result = (data.diff() > 0).sum()
    return result


def part2():
    data = pd.Series(inputparser())
    sums = data.rolling(3).sum()
    diffs = sums.diff()
    result = (sums.diff() > 0).sum()
    return result


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
