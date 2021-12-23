"""The quick-n-dirty solution for part 1 of the puzzle"""
from itertools import product
from pathlib import Path

from ycecream import y as ic

TEST_INPUT = Path("example.txt").read_text()
MY_INPUT = Path("input.txt").read_text()

TEST_1_SOLUTION = 590784
TEST_2_SOLUTION = 0


def solve1(reboot_steps):
    cubes = set()

    for step in reboot_steps:
        x_min, x_max = step["x"]
        y_min, y_max = step["y"]
        z_min, z_max = step["z"]

        if all(
            (
                abs(x_min) <= 50,
                abs(y_min) <= 50,
                abs(z_min) <= 50,
                abs(x_max) <= 50,
                abs(y_max) <= 50,
                abs(z_max) <= 50,
            )
        ):

            step_coords = product(
                range(x_min, x_max + 1),
                range(y_min, y_max + 1),
                range(z_min, z_max + 1),
            )

            if step["direction"] == "on":
                cubes = cubes.union(step_coords)
            else:
                cubes = cubes.difference(step_coords)
    return len(cubes)


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
    # turn on debug print statements
    ic.enabled = True
    result = solve1(parsetext(TEST_INPUT))
    assert result == TEST_1_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return solve1(parsetext(MY_INPUT))


result = part1()
print("Part 1: ", result)
