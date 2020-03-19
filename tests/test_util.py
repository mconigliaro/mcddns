import pytest as pt
import updatemyip.util as util


@pt.mark.parametrize(
    "original, prefix, result",
    [
        ["test", None, "test"],
        ["test_test", "test_", "test"],
        ["foo_test", "otherprefix", "foo_test"]
    ]
)
def test_strip_prefix(original, prefix, result):
    assert util.strip_prefix(original, prefix) == result


@pt.mark.parametrize(
    "original, prefix, result",
    [
        [int, None, "builtins.int"],
        [int, "built", "ins.int"],
    ]
)
def test_plugin_full_name(original, prefix, result):
    assert util.plugin_full_name(original, prefix) == result


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
