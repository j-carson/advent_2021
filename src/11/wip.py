from itertools import count
from pathlib import Path

import numpy as np
from ycecream import y as ic

MINI_TEST_INPUT = """11111
19991
19191
19991
11111"""

TEST_INPUT = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"""
TEST_1_SOLUTION_10 = 204
TEST_1_SOLUTION = 1656
TEST_2_SOLUTION = 195


class OctoGrid:
    def __init__(self, grid):
        self.grid = grid
        self.maxrow, self.maxcol = grid.shape

    def flash(self, row, col):
        row_above = max(row - 1, 0)
        row_below = min(row + 2, self.maxrow)

        col_left = max(col - 1, 0)
        col_right = min(col + 2, self.maxcol)

        # so we're never > 9 again this cycle
        self.grid[row, col] = np.nan

        for irow in range(row_above, row_below):
            for icol in range(col_left, col_right):
                self.grid[irow, icol] += 1

                if self.grid[irow, icol] > 9:
                    self.flash(irow, icol)

    def cycle(self):
        self.grid += 1

        for row in range(self.maxrow):
            for col in range(self.maxcol):
                if self.grid[row, col] > 9:
                    self.flash(row, col)

        n_flashes = np.isnan(self.grid).sum()
        self.grid[np.isnan(self.grid)] = 0
        return n_flashes


def solve1(grid, nsteps=100):
    result = 0
    for i in range(nsteps):
        result += grid.cycle()
    return result


def solve2(grid):
    for step in count(1):
        grid.cycle()
        if np.sum(grid.grid) == 0:
            return step


def parsetext(text):
    lines = text.splitlines()
    data = np.array([[int(i) for i in line] for line in lines]).astype(float)
    return OctoGrid(data)


def mydata():
    return Path("input.txt").read_text()


def part1():
    # turn on debug print statements
    ic.enabled = True
    result = solve1(parsetext(TEST_INPUT), 10)
    assert result == TEST_1_SOLUTION_10

    result = solve1(parsetext(TEST_INPUT), 100)
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
