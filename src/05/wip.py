import re
from collections import defaultdict, namedtuple
from pathlib import Path

import numpy as np
from ycecream import y

Point = namedtuple("Point", "x,y")


def generate_points(start, end):
    xstep = np.sign(end.x - start.x)
    ystep = np.sign(end.y - start.y)

    nextpoint = start
    while True:
        yield nextpoint
        if nextpoint == end:
            return
        nextpoint = Point(nextpoint.x + xstep, nextpoint.y + ystep)


def solve1(startpts, endpts, part2flag=False):
    result = defaultdict(int)

    for start, end in zip(startpts, endpts):
        if (start.x != end.x) and (start.y != end.y):
            if part2flag:
                for point in generate_points(start, end):
                    result[point] += 1
        else:
            for point in generate_points(start, end):
                result[point] += 1

    score = sum([val >= 2 for val in result.values()])
    return score


def solve2(startpts, endpts):
    return solve1(startpts, endpts, True)


def parsetext(text):
    numre = re.compile(r"(\d+)")
    lines = text.splitlines()
    startpts = []
    endpts = []
    for line in lines:
        x1, y1, x2, y2 = [int(i) for i in numre.findall(line)]

        startpts.append(Point(x1, y1))
        endpts.append(Point(x2, y2))
    return startpts, endpts


def testdata():
    return """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
"""


def mydata():
    return Path("input.txt").read_text()


def part1():
    test_solution = 5
    result = solve1(*parsetext(testdata()))
    assert result == test_solution

    return solve1(*parsetext(mydata()))


def part2():
    test_solution = 12
    result = solve2(*parsetext(testdata()))
    assert result == test_solution

    return solve2(*parsetext(mydata()))


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
