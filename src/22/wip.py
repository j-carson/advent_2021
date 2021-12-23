"""
Trying to be more efficient for part 2.
This one's not done -- part 1 puzzle can be solved
with the new algorithm, but part 2 still fails
"""


from dataclasses import dataclass
from itertools import product
from pathlib import Path
from typing import NamedTuple

from ycecream import y as ic

TOY_INPUT = """on x=10..12,y=10..12,z=10..12
on x=11..13,y=11..13,z=11..13
off x=9..11,y=9..11,z=9..11
on x=10..10,y=10..10,z=10..10"""
TEST_INPUT = Path("example.txt").read_text()
MY_INPUT = Path("input.txt").read_text()

TOY_SOLUTION = 39
TEST_1_SOLUTION = 590784
TEST_2_SOLUTION = 2758514936282235


class Coord(NamedTuple):
    x: int
    y: int
    z: int


class ValueRange(NamedTuple):
    low: int
    high: int

    def contains(self, value):
        return self.low <= value <= self.high

    @property
    def width(self):
        return self.high - self.low + 1


@dataclass
class Cube:
    state: str
    x_range: ValueRange
    y_range: ValueRange
    z_range: ValueRange

    def contains(self, coord):
        return (
            self.x_range.contains(coord.x)
            and self.y_range.contains(coord.y)
            and self.z_range.contains(coord.z)
        )


class OverlappingCubes:
    __slots__ = ["cubes", "x_changepts", "y_changepts", "z_changepts"]

    def __init__(self):
        self.cubes = []
        self.x_changepts = [ValueRange(-100_000, 100_000)]
        self.y_changepts = [ValueRange(-100_000, 100_000)]
        self.z_changepts = [ValueRange(-100_000, 100_000)]

    @staticmethod
    def update_changepts(new_range, changepts):
        low, high = new_range

        # need to create breaks in the change points so that the new
        # range is isolated
        # .., low-1) (low, ..) (...) (.., high) (high + 1, ..)
        for i, changept in enumerate(changepts):
            if changept.contains(low - 1):
                # there could already be a break where we want it...
                if changept[1] != low - 1:
                    changepts[i : i + 1] = ValueRange(changept[0], low - 1), ValueRange(
                        low, changept[1]
                    )
                break

        for i, changept in enumerate(changepts):
            if changept.contains(high):
                if changept[1] != high:
                    changepts[i : i + 1] = ValueRange(changept[0], high), ValueRange(
                        high + 1, changept[1]
                    )
                break

    def add_cube(self, cube):
        self.cubes.append(cube)
        self.update_changepts(cube.x_range, self.x_changepts)
        self.update_changepts(cube.y_range, self.y_changepts)
        self.update_changepts(cube.z_range, self.z_changepts)

    def count_on(self):
        total = 0
        for xs, ys, zs in product(self.x_changepts, self.y_changepts, self.z_changepts):

            coord = Coord(xs[0], ys[0], zs[0])
            subcubes = [cube for cube in self.cubes if cube.contains(coord)]

            if subcubes and (subcubes[-1].state == "on"):
                total += xs.width * ys.width * zs.width
        return total


def solve(reboot_steps, small_case=False):

    puzzle = OverlappingCubes()
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

            puzzle.add_cube(
                Cube(
                    step["direction"],
                    ValueRange(*step["x"]),
                    ValueRange(*step["y"]),
                    ValueRange(*step["z"]),
                )
            )
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
    ic.enabled = False
    result = solve(parsetext(TOY_INPUT), small_case=True)
    assert result == TOY_SOLUTION

    result = solve(parsetext(TEST_INPUT), small_case=True)
    assert result == TEST_1_SOLUTION

    return solve(parsetext(MY_INPUT), small_case=True)


def part2():
    ic.enabled = False
    result = solve(parsetext(TEST_INPUT), small_case=False)
    assert result == TEST_2_SOLUTION

    # turn off debug print statements
    return solve(parsetext(MY_INPUT), small_case=False)


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
