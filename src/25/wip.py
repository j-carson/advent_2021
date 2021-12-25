from itertools import count
from pathlib import Path

import numpy as np
from ycecream import y as ic

MY_INPUT = Path("input.txt").read_text().splitlines()
TEST_1_SOLUTION = 0
TEST_2_SOLUTION = 0


def move_east(east_arr, south_arr):
    rows, columns = east_arr.shape
    next_col = [(c + 1) % columns for c in range(columns)]

    can_go = np.empty((rows, columns), dtype=int)
    for current, dest in zip(range(columns), next_col):
        can_go[:, current] = east_arr[:, current] & (
            ~(east_arr[:, dest] | south_arr[:, dest])
        )

    movers = np.sum(can_go)

    if movers:
        for current, dest in zip(range(columns), next_col):
            column = can_go[:, current]
            east_arr[column == 1, current] = 0
            east_arr[column == 1, dest] = 1

    assert np.sum(east_arr & south_arr) == 0
    return movers


def move_south(east_arr, south_arr):
    rows, columns = south_arr.shape
    next_row = [(r + 1) % rows for r in range(rows)]

    can_go = np.empty((rows, columns), dtype=int)
    for current, dest in zip(range(rows), next_row):
        can_go[current, :] = south_arr[current, :] & (
            ~(east_arr[dest, :] | south_arr[dest, :])
        )

    movers = np.sum(can_go)

    if movers:
        for current, dest in zip(range(rows), next_row):
            row = can_go[current, :]
            south_arr[current, row == 1] = 0
            south_arr[dest, row == 1] = 1

    assert np.sum(east_arr & south_arr) == 0
    return movers


def test_part1():
    DATA = """v...>>.vv>
.vv>>.vv..
>>.>v>...v
>>v>>.>.v.
v>v.vv.v..
>.>>..v...
.vv..>.>v.
v.v..>>v.v
....v..v.>"""
    part1(DATA.splitlines(), debug=True)


def viz(east_cucumbers, south_cucumbers):
    rows, columns = east_cucumbers.shape

    for row in range(rows):
        for col in range(columns):
            if east_cucumbers[row, col]:
                print(">", end="")
            elif south_cucumbers[row, col]:
                print("v", end="")
            else:
                print(".", end="")
        print("\n", end="")
    print("\n", end="")


def part1(data, debug=False):
    east_decoder = {">": 1, ".": 0, "v": 0}
    south_decoder = {">": 0, ".": 0, "v": 1}
    east_cucumbers = np.array([[east_decoder[c] for c in line] for line in data])
    south_cucumbers = np.array([[south_decoder[c] for c in line] for line in data])

    if debug:
        viz(east_cucumbers, south_cucumbers)

    for turns in count(1):
        num_moved_east = move_east(east_cucumbers, south_cucumbers)
        num_moved_south = move_south(east_cucumbers, south_cucumbers)
        if (num_moved_east + num_moved_south) == 0:
            break

        if debug:
            viz(east_cucumbers, south_cucumbers)
            if turns > 5:
                break

    return turns


# test_part1()
result = part1(MY_INPUT)
print("Part 1: ", result)
