from collections import defaultdict
from pathlib import Path

import numpy as np
from ycecream import y


def generate_points(start, end):
    x1, y1 = start
    x2, y2 = end

    xstep = np.sign(x2 - x1)
    ystep = np.sign(y2 - y1)

    ix, iy = start
    while (ix != x2) or (iy != y2):
        yield (ix, iy)
        ix += xstep
        iy += ystep

    yield (ix, iy)


def solve1(startpts, endpts, part2flag=False):
    result = defaultdict(int)

    for start, end in zip(startpts, endpts):
        startx, starty = start
        endx, endy = end

        if (startx != endx) and (starty != endy):
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


def decode_tuple(coord):
    return np.array(coord.split(","), dtype=int)


def parsetext(text):
    lines = text.splitlines()
    startpts = []
    endpts = []
    for line in lines:
        points = line.split(" -> ")
        startpts.append(decode_tuple(points[0]))
        endpts.append(decode_tuple(points[1]))
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
