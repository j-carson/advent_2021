from collections import namedtuple
from pathlib import Path

import numpy as np
from ycecream import y as ic

TEST_INPUT = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5
"""

Dot = namedtuple("Dot", "x,y")
Fold = namedtuple("Fold", "axis,location")

TEST_1_SOLUTION = 17
TEST_2_SOLUTION = 0


class Paper:
    def __init__(self, dots):
        max_x = max([dot.x for dot in dots])
        max_y = max([dot.y for dot in dots])

        self.grid = np.zeros((max_y + 1, max_x + 1), dtype=int)
        for dot in dots:
            self.grid[dot.y, dot.x] = 1

    def fold_up(self, location):
        assert np.sum(self.grid[location, :]) == 0

        top_half = self.grid[0:location, :]
        bottom_half = np.flipud(self.grid[location + 1 :, :])

        self.grid = top_half | bottom_half

    def fold_left(self, location):
        assert np.sum(self.grid[:, location]) == 0

        left_half = self.grid[:, 0:location]
        right_half = np.fliplr(self.grid[:, location + 1 :])

        self.grid = left_half | right_half

    def fold(self, instruction):
        if instruction.axis == "x":
            self.fold_left(instruction.location)
        else:
            self.fold_up(instruction.location)

    def __repr__(self):
        show = " #"
        return "\n".join("".join([show[i] for i in line]) for line in self.grid)


def solve1(dots, folds):
    paper = Paper(dots)
    paper.fold(folds[0])
    return np.sum(paper.grid)


def solve2(dots, folds):
    paper = Paper(dots)
    for fold in folds:
        paper.fold(fold)
    print(paper)
    return 0


def parsetext(text):
    chunks = text.split("\n\n")

    dots = []
    for dot in chunks[0].splitlines():
        x, y = dot.split(",")
        dots.append(Dot(int(x), int(y)))

    folds = []
    for fold in chunks[1].splitlines():
        axis, location = fold.split()[-1].split("=")
        folds.append(Fold(axis, int(location)))

    return dots, folds


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
