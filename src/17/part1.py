from itertools import count

import numpy as np
from ycecream import y as ic

TEST_XMIN = 20
TEST_XMAX = 30
TEST_YMIN = -10
TEST_YMAX = -5

MY_XMIN = 96
MY_XMAX = 125
MY_YMIN = -144
MY_YMAX = -98


def find_v0x_min(xmin, xmax):
    """Find the initial x-velocity that just barely
    gets you to xmin - the idea is that we want to
    "stall out" over the range in x so we have time
    to go higher in y
    """

    def try_vx(vx):
        x = 0
        while vx > 0 and x <= xmax:
            x += vx
            vx -= np.sign(vx)
            if xmin <= x <= xmax:
                return True
        return False

    for vx in count(1):
        if try_vx(vx):
            return vx


def between(i, lo, high):
    return lo <= i <= high


def path(v0x, v0y, xmin, xmax, ymin, ymax):
    x = 0
    y = 0
    vx = v0x
    vy = v0y

    t = 0
    maxy = y

    ic.enabled = False
    while True:
        ic(t, x, y, vx, vy)
        t += 1
        x += vx
        y += vy
        vx -= np.sign(vx)
        vy -= 1
        maxy = max([maxy, y])

        if between(x, xmin, xmax) and between(y, ymin, ymax):
            ic.enabled = True
            ic(t, x, y, vx, vy)
            return maxy

        if y <= ymax and y <= ymin:
            return -1


def find_v0y_max(v0x, xmin, xmax, ymin, ymax):
    """We have the initial velocity in x, now search in y.
    A "definitely too fast" starting value to start searching
    at is abs(ymax) + 1
    """
    for v0y in count(abs(ymin) + 1, -1):
        vy_max = path(v0x, v0y, xmin, xmax, ymin, ymax)
        if vy_max != -1:
            print(v0y, vy_max)
            return vy_max


assert find_v0x_min(TEST_XMIN, TEST_XMAX) == 6
assert find_v0y_max(6, TEST_XMIN, TEST_XMAX, TEST_YMIN, TEST_YMAX) == 45

v0x = find_v0x_min(MY_XMIN, MY_XMAX)
print(find_v0y_max(v0x, MY_XMIN, MY_XMAX, MY_YMIN, MY_YMAX))
