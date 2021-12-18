from itertools import count, product

import numpy as np

TEST_XMIN = 20
TEST_XMAX = 30
TEST_YMIN = -10
TEST_YMAX = -5

MY_XMIN = 96
MY_XMAX = 125
MY_YMIN = -144
MY_YMAX = -98


def between(i, lo, high):
    return lo <= i <= high


def solution_search(xmin, xmax, ymin, ymax):

    vx_min = 0
    vx_max = xmax
    vy_min = ymin
    vy_max = abs(ymin)

    def try_solution(v0x, v0y):
        x = 0
        y = 0
        vx = v0x
        vy = v0y

        while True:
            x += vx
            y += vy
            vx -= np.sign(vx)
            vy -= 1
            if between(x, xmin, xmax) and between(y, ymin, ymax):
                return 1
            if (vx == 0) and (not between(x, xmin, xmax)):
                return 0
            if y < ymin:
                return 0
            if x > xmax:
                return 0

    total = 0
    for v0x, v0y in product(range(vx_min, vx_max + 1), range(vy_min, vy_max + 1)):
        total += try_solution(v0x, v0y)
    return total


assert solution_search(TEST_XMIN, TEST_XMAX, TEST_YMIN, TEST_YMAX) == 112

print(solution_search(MY_XMIN, MY_XMAX, MY_YMIN, MY_YMAX))
