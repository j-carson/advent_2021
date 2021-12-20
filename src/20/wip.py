from pathlib import Path

import numpy as np
from ycecream import y as ic

TEST_INPUT = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###
"""
TEST_1_SOLUTION = 35
TEST_2_SOLUTION = 3351


def make_binary(flags):
    nums = "01"
    binary = int("".join([nums[i] for i in flags]), 2)
    return binary


def enhance1(enhance, image, background=0):

    padimage = np.pad(image, 2, constant_values=background)

    row_range = (0, padimage.shape[0] - 2)
    col_range = (0, padimage.shape[1] - 2)

    new_image = np.zeros(padimage.shape, dtype=int)
    for i in range(*row_range):
        for j in range(*col_range):
            sub_array = padimage[i : i + 3, j : j + 3].flatten()
            index = make_binary(sub_array)
            new_image[i, j] = enhance[index]

    new_image = new_image[0:-2, 0:-2]
    new_background = enhance[make_binary([background] * 9)]

    return new_image, new_background


def solve1(enhance, image):
    ic(image.shape)
    im, bg = enhance1(enhance, image, 0)
    im2, bg = enhance1(enhance, im, bg)
    return np.sum(im2)


def solve2(enhance, image):
    im, bg = image, 0
    for i in range(50):
        im, bg = enhance1(enhance, im, bg)
    return np.sum(im)


def parsetext(text):
    chunks = text.split("\n\n")
    num = {"#": 1, ".": 0}
    enhance = [num[ch] for ch in chunks[0]]
    assert len(enhance) == 512

    image = []
    for line in chunks[1].splitlines():
        image.append([num[ch] for ch in line])
    return enhance, np.array(image)


def mydata():
    return Path("input.txt").read_text()


def part1():
    # turn on debug print statements
    ic.enabled = False
    result = solve1(*parsetext(TEST_INPUT))
    assert result == TEST_1_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return solve1(*parsetext(mydata()))


def part2():

    # turn on debug print statements
    ic.enabled = False
    result = solve2(*parsetext(TEST_INPUT))
    assert result == TEST_2_SOLUTION

    # turn off debug print statements
    ic.enabled = False
    return solve2(*parsetext(mydata()))


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
