from functools import cache


@cache
def func0(w, x, y, z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + 12) == INPUT) == 0),
        INPUT,
        (z * ((25 * int(int(((z % 26) + 12) == INPUT) == 0)) + 1)),
    )


@cache
def func1(w, x, y, z):
    return w, x, ((y + 7) * x), (z + ((y + 7) * x))


@cache
def func2(w, x, y, z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + 11) == INPUT) == 0),
        INPUT,
        (z * ((25 * int(int(((z % 26) + 11) == INPUT) == 0)) + 1)),
    )


@cache
def func3(w, x, y, z):
    return w, x, ((y + 15) * x), (z + ((y + 15) * x))


@cache
def func4(w, x, y, z):
    return w, x, ((y + 2) * x), (z + ((y + 2) * x))


@cache
def func5(w, x, y, z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + -3) == INPUT) == 0),
        INPUT,
        ((z // 26) * ((25 * int(int(((z % 26) + -3) == INPUT) == 0)) + 1)),
    )


@cache
def func6(w, x, y, z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + 10) == INPUT) == 0),
        INPUT,
        (z * ((25 * int(int(((z % 26) + 10) == INPUT) == 0)) + 1)),
    )


@cache
def func7(w, x, y, z):
    return w, x, ((y + 14) * x), (z + ((y + 14) * x))


@cache
def func8(w, x, y, z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + -9) == INPUT) == 0),
        INPUT,
        ((z // 26) * ((25 * int(int(((z % 26) + -9) == INPUT) == 0)) + 1)),
    )


@cache
def func9(w, x, y, z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + -7) == INPUT) == 0),
        INPUT,
        ((z // 26) * ((25 * int(int(((z % 26) + -7) == INPUT) == 0)) + 1)),
    )


@cache
def func10(w, x, y, z):
    return w, x, ((y + 1) * x), (z + ((y + 1) * x))


@cache
def func11(w, x, y, z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + -11) == INPUT) == 0),
        INPUT,
        ((z // 26) * ((25 * int(int(((z % 26) + -11) == INPUT) == 0)) + 1)),
    )


@cache
def func12(w, x, y, z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + -4) == INPUT) == 0),
        INPUT,
        ((z // 26) * ((25 * int(int(((z % 26) + -4) == INPUT) == 0)) + 1)),
    )


@cache
def func13(w, x, y, z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + 14) == INPUT) == 0),
        INPUT,
        (z * ((25 * int(int(((z % 26) + 14) == INPUT) == 0)) + 1)),
    )


@cache
def func14(w, x, y, z):
    return w, x, ((y + 12) * x), (z + ((y + 12) * x))


@cache
def func15(w, x, y, z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + -8) == INPUT) == 0),
        INPUT,
        ((z // 26) * ((25 * int(int(((z % 26) + -8) == INPUT) == 0)) + 1)),
    )


@cache
def func16(w, x, y, z):
    return w, x, ((y + 13) * x), (z + ((y + 13) * x))


@cache
def func17(w, x, y, z, INPUT):
    return (
        INPUT,
        int(int(((z % 26) + -10) == INPUT) == 0),
        INPUT,
        ((z // 26) * ((25 * int(int(((z % 26) + -10) == INPUT) == 0)) + 1)),
    )


def eval_license(INPUTS):
    w = x = y = z = 0
    INPUT_ITERATOR = INPUTS.__iter__()
    INPUT = next(INPUT_ITERATOR)
    w, x, y, z = func0(w, x, y, z, INPUT)
    w, x, y, z = func1(w, x, y, z)
    INPUT = next(INPUT_ITERATOR)
    w, x, y, z = func2(w, x, y, z, INPUT)
    w, x, y, z = func3(w, x, y, z)
    INPUT = next(INPUT_ITERATOR)
    w, x, y, z = func0(w, x, y, z, INPUT)
    w, x, y, z = func4(w, x, y, z)
    INPUT = next(INPUT_ITERATOR)
    w, x, y, z = func5(w, x, y, z, INPUT)
    w, x, y, z = func3(w, x, y, z)
    INPUT = next(INPUT_ITERATOR)
    w, x, y, z = func6(w, x, y, z, INPUT)
    w, x, y, z = func7(w, x, y, z)
    INPUT = next(INPUT_ITERATOR)
    w, x, y, z = func8(w, x, y, z, INPUT)
    w, x, y, z = func4(w, x, y, z)
    INPUT = next(INPUT_ITERATOR)
    w, x, y, z = func6(w, x, y, z, INPUT)
    w, x, y, z = func3(w, x, y, z)
    INPUT = next(INPUT_ITERATOR)
    w, x, y, z = func9(w, x, y, z, INPUT)
    w, x, y, z = func10(w, x, y, z)
    INPUT = next(INPUT_ITERATOR)
    w, x, y, z = func11(w, x, y, z, INPUT)
    w, x, y, z = func3(w, x, y, z)
    INPUT = next(INPUT_ITERATOR)
    w, x, y, z = func12(w, x, y, z, INPUT)
    w, x, y, z = func3(w, x, y, z)
    INPUT = next(INPUT_ITERATOR)
    w, x, y, z = func13(w, x, y, z, INPUT)
    w, x, y, z = func14(w, x, y, z)
    INPUT = next(INPUT_ITERATOR)
    w, x, y, z = func2(w, x, y, z, INPUT)
    w, x, y, z = func4(w, x, y, z)
    INPUT = next(INPUT_ITERATOR)
    w, x, y, z = func15(w, x, y, z, INPUT)
    w, x, y, z = func16(w, x, y, z)
    INPUT = next(INPUT_ITERATOR)
    w, x, y, z = func17(w, x, y, z, INPUT)
    w, x, y, z = func16(w, x, y, z)
    return z == 0
