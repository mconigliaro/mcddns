import itertools as it
import pytest as pt
import updatemyip.validator as val


@pt.mark.parametrize(
    "value, result",
    [
        ["127.0.0.1", True],
        ["::1", True],
        ["test", False]
    ]
)
def test_ip_address(value, result):
    assert val.ip_address(value) == result


@pt.mark.parametrize(
    "value, result",
    [
        ["127.0.0.1", True],
        ["::1", False],
        ["test", False]
    ]
)
def test_ipv4_address(value, result):
    assert val.ipv4_address(value) == result


@pt.mark.parametrize(
    "value, result",
    [
        ["::1", True],
        ["127.0.0.1", False],
        ["test", False]
    ]
)
def test_ipv6_address(value, result):
    assert val.ipv6_address(value) == result


@pt.mark.parametrize(
    "value, result",
    [
        ["foo.bar.", True],
        [str(it.repeat("x", 256)), False],
        ["fail!", False]
    ]
)
def test_hostname(value, result):
    assert val.hostname(value) == result
