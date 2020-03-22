import itertools as it
import pytest as pt
import updatemyip.provider_util as pru


@pt.mark.parametrize(
    "url, result",
    [
        ["http://example.com/",
         "The requested URL was not found on this server."]
    ]
)
def test_fetch_url(url, result):
    assert pru.fetch_url(url) == result


@pt.mark.parametrize(
    "value, result",
    [
        ["127.0.0.1", True],
        ["::1", True],
        ["test", False]
    ]
)
def test_is_ip_address(value, result):
    assert pru.is_ip_address(value) == result


@pt.mark.parametrize(
    "value, result",
    [
        ["127.0.0.1", True],
        ["::1", False],
        ["test", False]
    ]
)
def test_is_ipv4_address(value, result):
    assert pru.is_ipv4_address(value) == result


@pt.mark.parametrize(
    "value, result",
    [
        ["::1", True],
        ["127.0.0.1", False],
        ["test", False]
    ]
)
def test_is_ipv6_address(value, result):
    assert pru.is_ipv6_address(value) == result


@pt.mark.parametrize(
    "value, result",
    [
        ["foo.bar.", True],
        [str(it.repeat("x", 256)), False],
        ["fail!", False]
    ]
)
def test_is_hostname(value, result):
    assert pru.is_hostname(value) == result
