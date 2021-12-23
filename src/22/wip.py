from pathlib import Path
from typing import NamedTuple

import numpy as np

TOY_INPUT = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""
TEST_INPUT = Path("example.txt").read_text()
TEST_2_INPUT = Path("example2.txt").read_text()
MY_INPUT = Path("input.txt").read_text()

TOY_SOLUTION = 39
TEST_1_SOLUTION = 590784
TEST_2_SOLUTION = 2758514936282235


class ValueRange(NamedTuple):
    low: int
    high: int

    def contains(self, value):
        return self.low <= value <= self.high


class Cube(NamedTuple):
    state: str
    x_range: ValueRange
    y_range: ValueRange
    z_range: ValueRange


class OverlappingCubes:
    __slots__ = [
        "cubes",
        "x_changepts",
        "y_changepts",
        "z_changepts",
    ]

    def __init__(self, cubes):
        self.cubes = cubes

        self.x_changepts = []
        self.y_changepts = []
        self.z_changepts = []

        for c in cubes:
            # we need to start new evaluation area where the range
            # starts and one spot after where it ends
            self.x_changepts.extend([c.x_range[0], c.x_range[1] + 1])
            self.y_changepts.extend([c.y_range[0], c.y_range[1] + 1])
            self.z_changepts.extend([c.z_range[0], c.z_range[1] + 1])

        # np.unique filters duplicates and sorts in one step!
        self.x_changepts = np.unique(self.x_changepts)
        self.y_changepts = np.unique(self.y_changepts)
        self.z_changepts = np.unique(self.z_changepts)

    def count_on(self):
        total = 0
        for x, x_next in zip(self.x_changepts, self.x_changepts[1:]):
            x_width = x_next - x
            x_cubes = [c for c in self.cubes if c.x_range.contains(x)]

            for y, y_next in zip(self.y_changepts, self.y_changepts[1:]):
                y_width = y_next - y
                xy_cubes = [c for c in x_cubes if c.y_range.contains(y)]

                for z, z_next in zip(self.z_changepts, self.z_changepts[1:]):
                    z_width = z_next - z

                    subcubes = [c for c in xy_cubes if c.z_range.contains(z)]
                    if subcubes and (subcubes[-1].state == "on"):
                        total += x_width * y_width * z_width

        return total


def solve(reboot_steps, small_case=False):

    cubes = []

    for step in reboot_steps:
        if (not small_case) or all(
            (
                small_case,
                abs(step["x"][0]) <= 50,
                abs(step["y"][0]) <= 50,
                abs(step["z"][0]) <= 50,
                abs(step["x"][1]) <= 50,
                abs(step["y"][1]) <= 50,
                abs(step["z"][1]) <= 50,
            )
        ):

            cubes.append(
                Cube(
                    step["direction"],
                    ValueRange(*step["x"]),
                    ValueRange(*step["y"]),
                    ValueRange(*step["z"]),
                )
            )

    puzzle = OverlappingCubes(cubes)
    return puzzle.count_on()


def parsetext(text):
    result = []
    lines = text.splitlines()
    for line in lines:
        d = {}
        words = line.split()
        d["direction"] = words[0].strip()
        ranges = words[1].split(",")
        for r in ranges:
            which = r[0]
            vals = [int(i) for i in r[2:].split("..")]
            d[which] = vals
        result.append(d)
    return result


def part1():
    result = solve(parsetext(TOY_INPUT), small_case=True)
    assert result == TOY_SOLUTION

    result = solve(parsetext(TEST_INPUT), small_case=True)
    assert result == TEST_1_SOLUTION

    return solve(parsetext(MY_INPUT), small_case=True)


def part2():
    result = solve(parsetext(TEST_2_INPUT), small_case=False)
    print("test 2:", result, TEST_2_SOLUTION)
    assert result == TEST_2_SOLUTION

    # turn off debug print statements
    return solve(parsetext(MY_INPUT), small_case=False)


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
