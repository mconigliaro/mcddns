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
    "attempt, delay",
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
def test_backoff(attempt, delay):
    assert util.backoff(attempt, no_delay=True) == delay
