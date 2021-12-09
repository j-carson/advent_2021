from pathlib import Path

import numpy as np
import pandas as pd
from ycecream import y as ic

TEST_INPUT = """2199943210
3987894921
9856789892
8767896789
9899965678"""

TEST_1_SOLUTION = 15
TEST_2_SOLUTION = 1134


def get_low_points(df):
    up = df.diff().fillna(-99)
    down = df.diff(periods=-1).fillna(-99)
    left = df.diff(axis=1).fillna(-99)
    right = df.diff(axis=1, periods=-1).fillna(-99)

    low_points = (down < 0) & (up < 0) & (left < 0) & (right < 0)
    return ic(low_points)


def solve1(df):
    low_points = get_low_points(df)
    # second sum is to change a series to a scalar
    risk_level = low_points.sum().sum() + df[low_points].sum().sum()
    ic(risk_level)

    return risk_level


def copy_positive_neighbor(row, col, basins):
    maxrow, maxcol = basins.shape
    if col > 0 and basins[row, col - 1] > 0:
        basins[row, col] = basins[row, col - 1]
    if (col + 1) < maxcol and basins[row, col + 1] > 0:
        basins[row, col] = basins[row, col + 1]
    if row > 0 and basins[row - 1, col] > 0:
        basins[row, col] = basins[row - 1, col]
    if (row + 1) < maxrow and basins[row + 1, col] > 0:
        basins[row, col] = basins[row + 1, col]


def solve2(df):
    low_points = get_low_points(df)
    low_rows, low_columns = np.where(low_points)

    basins = np.zeros(df.shape)
    basins[(df == 9).to_numpy()] = -1

    for basin_id, coord in enumerate(zip(low_rows, low_columns)):
        row, column = coord
        basin_id += 1
        basins[row, column] = basin_id

    ic(basins)
    done = 1
    while done != 0:
        rows, cols = np.where(basins == 0)
        for row, col in zip(rows, cols):
            copy_positive_neighbor(row, col, basins)

        done = np.sum(basins == 0)
        ic(done, basins)

    values, counts = np.unique(basins, return_counts=True)
    ic(values, counts)
    # Don't count the nines, which have value == -1
    counts = counts[values > 0]

    ic(values, counts)
    top3 = np.sort(counts)[-3:]
    return np.prod(top3)


def parsetext(text):
    result = pd.DataFrame([[int(n) for n in list(line)] for line in text.splitlines()])
    return ic(result)


def mydata():
    return Path("input.txt").read_text()


def part1():
    # turn on debug print statements
    ic.enabled = False
    result = solve1(parsetext(TEST_INPUT))
    assert result == TEST_1_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return solve1(parsetext(mydata()))


def part2():

    # turn on debug print statements
    ic.enabled = False
    result = solve2(parsetext(TEST_INPUT))
    assert result == TEST_2_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return solve2(parsetext(mydata()))


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
