import copy

def repeated(f):
    """
    >>> double = lambda x: 2 * x
    >>> funcs = repeated(double)
    >>> identity = next(funcs)
    >>> double = next(funcs)
    >>> quad = next(funcs)
    >>> oct = next(funcs)
    >>> quad(1)
    4
    >>> oct(1)
    8
    >>> [g(1) for _, g in
    ...  zip(range(5), repeated(lambda x: 2 * x))]
    [1, 2, 4, 8, 16]
    """

    def helper(f, times):
        if times == 0:
            return lambda x: x
        else:
            return lambda x: f(helper(f, (times-1))(x))

    times = 0
    while True:
        yield helper(f, times)
        times += 1


double = lambda x: 2 * x
funcs = repeated(double)
identity = next(funcs)
double = next(funcs)
quad = next(funcs)
oct = next(funcs)
assert quad(1) == 4
assert oct(1) == 8
assert [g(1) for _, g in zip(range(5), repeated(lambda x: 2 * x))] == [1, 2, 4, 8, 16]
print("you did it!")
