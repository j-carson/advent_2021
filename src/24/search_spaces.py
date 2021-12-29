from itertools import product


def search_space():
    # right hand sides of inequalities
    range_7 = range(9, 0, -1)
    range_12 = range(9, 0, -1)
    range_5 = range(9, 0, -1)
    range_8 = range(9, 0, -1)
    range_9 = range(9, 0, -1)
    range_13 = range(9, 0, -1)
    range_3 = range(9, 0, -1)

    # left hand sides of inequalities
    range_6 = (1, 0, -1)  # inputs[6] + 8 between 1 and 9
    range_11 = (9, 5, -1)  # inputs[11] - 6 between 1 and 9
    range_4 = (4, 0, -1)  # inputs[11] + 5 between 1 and 9
    range_1 = (5, 0, -1)  # inputs[1] + 4 between 1 and 9
    range_0 = (6, 0, -1)
    range_10 = (7, 0, -1)
    range_2 = (9, 1, -1)
    return product(
        range_0,
        range_1,
        range_2,
        range_3,
        range_4,
        range_5,
        range_6,
        range_7,
        range_8,
        range_9,
        range_10,
        range_11,
        range_12,
        range_13,
    )


def search_space2():
    # right hand sides of inequalities, searching lowest to highest
    range_7 = range(1, 10)
    range_12 = range(1, 10)
    range_5 = range(1, 10)
    range_8 = range(1, 10)
    range_9 = range(1, 10)
    range_13 = range(1, 10)
    range_3 = range(1, 10)

    # left hand sides of inequalities
    range_6 = (1, 2)
    range_11 = (7, 10)
    range_4 = (1, 5)
    range_1 = (1, 6)
    range_0 = (1, 7)
    range_10 = (1, 8)
    range_2 = (2, 10)
    return product(
        range_0,
        range_1,
        range_2,
        range_3,
        range_4,
        range_5,
        range_6,
        range_7,
        range_8,
        range_9,
        range_10,
        range_11,
        range_12,
        range_13,
    )
