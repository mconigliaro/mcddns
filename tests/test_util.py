import pytest as pt
import updatemyip.util as util


@pt.mark.parametrize(
    "n, fib",
    [
        [0, 1],
        [1, 1],
        [2, 2],
        [3, 3],
        [4, 5],
        [5, 8],
        [6, 13],
        [7, 21],
        [8, 34],
        [9, 55]
    ]
)
def test_fibonacci_backoff(n, fib):
    assert util.fibonacci_backoff(n, sleep=False) == fib
