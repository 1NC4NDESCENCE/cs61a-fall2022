from operator import add, mul

square = lambda x: x * x

identity = lambda x: x

triple = lambda x: 3 * x

increment = lambda x: x + 1


def ordered_digits(x):
    """Return True if the (base 10) digits of X>0 are in non-decreasing
    order, and False otherwise.

    >>> ordered_digits(5)
    True
    >>> ordered_digits(11)
    True
    >>> ordered_digits(127)
    True
    >>> ordered_digits(1357)
    True
    >>> ordered_digits(21)
    False
    >>> result = ordered_digits(1375) # Return, don't print
    >>> result
    False

    """
    last_digit = x % 10
    x //= 10
    while x:
        digit = x % 10
        if last_digit < digit:
            return False
        x //= 10
    return True


def get_k_run_starter(n, k):
    """Returns the 0th digit of the kth increasing run within n.
    >>> get_k_run_starter(123444345, 0) # example from description
    3
    >>> get_k_run_starter(123444345, 1)
    4
    >>> get_k_run_starter(123444345, 2)
    4
    >>> get_k_run_starter(123444345, 3)
    1
    >>> get_k_run_starter(123412341234, 1)
    1
    >>> get_k_run_starter(1234234534564567, 0)
    4
    >>> get_k_run_starter(1234234534564567, 1)
    3
    >>> get_k_run_starter(1234234534564567, 2)
    2
    """
#    n //= 10
#    while n:
#        digit = n % 10
#        if last_digit <= digit:
#            if k == n_th:
#                return last_digit
#            n_th += 1
#        n //= 10
    n_th = 0
    last_digit = 10
    digit = n % 10
    start = -1
    while n_th <=k:
        while last_digit > digit and digit:
            last_digit = digit
            n //= 10
            digit = n % 10
        start = last_digit
        last_digit = digit
        n //= 10
        digit = n % 10
        n_th += 1
    return start
#    while ____________________________:
#        while ____________________________:
#            ____________________________
#        final = ____________________________
#        i = ____________________________
#        n = ____________________________
#    return final


def make_repeater(func, n):
    """Return the function that computes the nth application of func.

    >>> add_three = make_repeater(increment, 3)
    >>> add_three(5)
    8
    >>> make_repeater(triple, 5)(1) # 3 * 3 * 3 * 3 * 3 * 1
    243
    >>> make_repeater(square, 2)(5) # square(square(5))
    625
    >>> make_repeater(square, 4)(5) # square(square(square(square(5))))
    152587890625
    >>> make_repeater(square, 0)(5) # Yes, it makes sense to apply the function zero times!
    5
    """
    if n == 0:
        return lambda x: x
    if n == 1:
        return func
    else:
        return lambda x: func(make_repeater(func, n-1)(x))


def composer(func1, func2):
    """Return a function f, such that f(x) = func1(func2(x))."""
    def f(x):
        return func1(func2(x))
    return f


def apply_twice(func):
    """ Return a function that applies func twice.

    func -- a function that takes one argument

    >>> apply_twice(square)(2)
    16
    """
    return composer(func, func)


def div_by_primes_under(n):
    """
    >>> div_by_primes_under(10)(11)
    False
    >>> div_by_primes_under(10)(121)
    False
    >>> div_by_primes_under(10)(12)
    True
    >>> div_by_primes_under(5)(1)
    False
    """
    return lambda x: any(x % i == 0 for i in range(2, n))
#    checker = lambda x: False
#    i = ____________________________
#    while ____________________________:
#        if not checker(i):
#            checker = ____________________________
#        i = ____________________________
#    return ____________________________


def div_by_primes_under_no_lambda(n):
    """
    >>> div_by_primes_under_no_lambda(10)(11)
    False
    >>> div_by_primes_under_no_lambda(10)(121)
    False
    >>> div_by_primes_under_no_lambda(10)(12)
    True
    >>> div_by_primes_under_no_lambda(5)(1)
    False
    """
    def check(num):
        for i in range(2, n):
            if num % i == 0:
                return True
        return False
    return check
#    def checker(x):
#        return False
#    i = ____________________________
#    while ____________________________:
#        if not checker(i):
#            def outer(____________________________):
#                def inner(____________________________):
#                    return ____________________________
#                return ____________________________
#            checker = ____________________________
#        i = ____________________________
#    return ____________________________


def zero(f):
    return lambda x: x


def successor(n):
    return lambda f: lambda x: f(n(f)(x))


def one(f):
    """Church numeral 1: same as successor(zero)"""
    return lambda x: f(x)


def two(f):
    """Church numeral 2: same as successor(successor(zero))"""
    return lambda x: f(f(x))


three = successor(two)


def church_to_int(n):
    """Convert the Church numeral n to a Python integer.

    >>> church_to_int(zero)
    0
    >>> church_to_int(one)
    1
    >>> church_to_int(two)
    2
    >>> church_to_int(three)
    3
    """
    return n(increment)(0)


def add_church(m, n):
    """Return the Church numeral for m + n, for Church numerals m and n.

    >>> church_to_int(add_church(two, three))
    5
    """
    return lambda f: lambda x: n(f)(m(f)(x))


def int_to_church(num):
    """Convert a Python integer to a Church numeral."""
    op = lambda f: lambda x: x
    for i in range(num):
        op = successor(op)
#        op = lambda f: lambda x: f(op(f)(x))
    return op


def mul_church(m, n):
    """Return the Church numeral for m * n, for Church numerals m and n.

    >>> four = successor(three)
    >>> church_to_int(mul_church(two, three))
    6
    >>> church_to_int(mul_church(three, four))
    12
    """
    num = church_to_int(m) * church_to_int(n)
    return int_to_church(num)



def pow_church(m, n):
    """Return the Church numeral m ** n, for Church numerals m and n.

    >>> church_to_int(pow_church(two, three))
    8
    >>> church_to_int(pow_church(three, two))
    9
    """
    num = church_to_int(m) ** church_to_int(n)
    return int_to_church(num)
