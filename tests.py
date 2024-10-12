from decorators import get_time
from decorators import memoize
import time
from functools import cache
import analytical_computations as ac


def fib(n: int):
    if n < 0:
        return ValueError("parameter [n] must be positive")
    if n == 0:
        return 1
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)


@memoize
def memoized_fib(n: int):
    if n < 0:
        return ValueError("parameter [n] must be positive")
    if n == 0:
        return 1
    if n == 1:
        return 1
    return fib(n-1) + fib(n-2)


if __name__ == "__main__":
    start = time.time()
    result = fib(25)
    end = time.time()
    print(f"non-memoized fib(25): {result}\n->execution time: {end - start}")

    start = time.time()
    result = memoized_fib(25)
    end = time.time()
    print(f"memoized fib(25): {result}\n->execution time: {end - start}")

    poly1 = ac.Polynomial(2, [1, 2, 3])
    poly2 = ac.Polynomial(1, [1, 2])

    print(f"poly1: {poly1}")
    print(f"poly2: {poly2}")

    print(f"poly1+poly2: {poly1 + poly2}")
    print(f"poly1*poly2: {poly1 * poly2}")
    print(f"d/dx(poly1): {poly1.d_dx()}")

