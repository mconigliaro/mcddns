import itertools
import pytest
import updatemyip.exceptions as exceptions
import updatemyip.provider as provider


def test_fetch_url():
    assert len(provider.AddressProvider.fetch_url("http://example.com"))


@pytest.mark.parametrize(
    "value, result",
    [
        ["127.0.0.1", True],
        ["::1", True],
        ["test", False]
    ]
)
def test_is_ip_address(value, result):
    assert provider.AddressProvider.is_ip_address(value) == result


@pytest.mark.parametrize(
    "value, result",
    [
        ["127.0.0.1", True],
        ["::1", False],
        ["test", False]
    ]
)
def test_is_ipv4_address(value, result):
    assert provider.AddressProvider.is_ipv4_address(value) == result


@pytest.mark.parametrize(
    "value, result",
    [
        ["::1", True],
        ["127.0.0.1", False],
        ["test", False]
    ]
)
def test_is_ipv6_address(value, result):
    assert provider.AddressProvider.is_ipv6_address(value) == result


@pytest.mark.parametrize(
    "value, result",
    [
        ["foo.bar.", True],
        [str(itertools.repeat("x", 256)), False],
        ["fail!", False]
    ]
)
def test_is_hostname(value, result):
    assert provider.AddressProvider.is_hostname(value) == result


@pytest.mark.parametrize(
    "original, prefix, result",
    [
        ["test", None, "test"],
        ["test_test", "test_", "test"],
        ["foo_test", "otherprefix", "foo_test"]
    ]
)
def test_strip_prefix(original, prefix, result):
    assert provider.strip_prefix(original, prefix) == result


@pytest.mark.parametrize(
    "original, result",
    [
        [int, "builtins.int"]
    ]
)
def test_provider_full_name(original, result):
    assert provider.provider_full_name(original) == result


@pytest.mark.parametrize(
    "types, providers",
    [
        [None,
            ["test.Address", "test.AddressFalse", "test.AddressError",
             "test.DNS", "test.DNSCheckFalse", "test.DNSCheckError",
             "test.DNSUpdateFalse"]],
        [provider.AddressProvider,
            ["test.Address", "test.AddressFalse", "test.AddressError"]],
        [provider.DNSProvider,
            ["test.DNS", "test.DNSCheckFalse", "test.DNSCheckError",
             "test.DNSUpdateFalse"]]
    ]
)
def test_list_providers(types, providers):
    assert list(provider.list_providers(types).keys()) == providers


def test_list_providers_invalid():
    with pytest.raises(exceptions.NoSuchProviderTypeError):
        provider.list_providers(int)


@pytest.mark.parametrize(
    "name, base_type",
    [
        ["test.Address", provider.AddressProvider],
        ["test.DNS", provider.DNSProvider]
    ]
)
def test_get_provider(name, base_type):
    assert base_type in provider.get_provider(name).__bases__


def test_get_provider_unknown():
    with pytest.raises(exceptions.NoSuchProviderError):
        provider.get_provider("test.unknown")
