import heapq
from itertools import product
from pathlib import Path
from typing import NamedTuple

import numpy as np
from ycecream import y as ic

TEST_INPUT = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"""

TEST_1_SOLUTION = 40
TEST_2_SOLUTION = 315


class Coord(NamedTuple):
    x: int
    y: int

    def neighbors(self, maxrow, maxcol):
        deltas = (Coord(-1, 0), Coord(1, 0), Coord(0, -1), Coord(0, 1))
        for delta in deltas:
            neighbor = Coord(self.x + delta.x, self.y + delta.y)
            if all(
                (
                    neighbor.x >= 0,
                    neighbor.x < maxrow,
                    neighbor.y >= 0,
                    neighbor.y < maxcol,
                )
            ):
                yield neighbor


def solve1(cavemap):

    # based on https://www.udacity.com/blog/2021/10/implementing-dijkstras-algorithm-in-python.html
    maxrow, maxcol = cavemap.shape

    weights = cavemap
    visited = np.zeros(cavemap.shape, dtype=int)

    shortest_path = np.empty(cavemap.shape, dtype=int)
    max_value = 10 * maxrow * maxcol
    shortest_path[:] = max_value

    worklist = []

    def add_to_worklist(node, distance):
        shortest_path[node.x, node.y] = distance
        heapq.heappush(worklist, (distance, node))

    def pop_worklist():
        while True:
            distance, coord = heapq.heappop(worklist)
            if visited[coord.x, coord.y]:
                continue
            if shortest_path[coord.x, coord.y] == distance:
                return distance, coord

    start_node = Coord(0, 0)
    add_to_worklist(start_node, 0)

    while not visited[maxrow - 1, maxcol - 1]:

        distance, current_min_node = pop_worklist()

        for neighbor in current_min_node.neighbors(maxrow, maxcol):
            tentative_value = shortest_path[current_min_node] + weights[neighbor]
            if tentative_value < shortest_path[neighbor]:
                add_to_worklist(neighbor, tentative_value)

        visited[current_min_node.x, current_min_node.y] = 1

    return shortest_path[Coord(maxrow - 1, maxcol - 1)]


def increment_tile(tile, count):
    new_tile = tile.copy()

    for i in range(1, count + 1):
        new_tile += 1
        new_tile[new_tile == 10] = 1

    return new_tile


def solve2(tile):
    cavemap = np.vstack(
        [
            np.hstack([increment_tile(tile, i) for i in range(5)]),
            np.hstack([increment_tile(tile, i) for i in range(1, 6)]),
            np.hstack([increment_tile(tile, i) for i in range(2, 7)]),
            np.hstack([increment_tile(tile, i) for i in range(3, 8)]),
            np.hstack([increment_tile(tile, i) for i in range(4, 9)]),
        ]
    )
    ic(cavemap)
    return solve1(cavemap)


def parsetext(text):
    result = np.array([[int(c) for c in line] for line in text.splitlines()])
    return ic(result)


def mydata():
    return Path("input.txt").read_text()


def part1():
    # turn on debug print statements
    ic.enabled = True
    result = solve1(parsetext(TEST_INPUT))
    assert result == TEST_1_SOLUTION
    ic("part 1 passed")

    # turn off debug print statements
    ic.enabled = False
    return solve1(parsetext(mydata()))


def part2():

    # turn on debug print statements
    ic.enabled = True
    result = solve2(parsetext(TEST_INPUT))
    assert result == TEST_2_SOLUTION
    ic("part 2 passed")

    # turn off debug print statements
    ic.enabled = False
    return solve2(parsetext(mydata()))


result = part1()
print("Part 1: ", result)

result = part2()
print("Part 2: ", result)
