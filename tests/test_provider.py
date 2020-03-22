import os
import pytest as pt
import updatemyip.exceptions as exc
import updatemyip.provider as pro


def test_import_modules():
    path = os.path.join(os.path.dirname(__file__), "providers")
    assert list(pro.import_modules(path).keys()) == ["updatemyip_test"]


@pt.mark.parametrize(
    "original, result",
    [
        [int, "builtins.int"]
    ]
)
def test_provider_full_name(original, result):
    assert pro.provider_full_name(original) == result


@pt.mark.parametrize(
    "types, providers",
    [
        [None,
            ["test.Address", "test.AddressFalse", "test.AddressError",
             "test.DNS", "test.DNSCheckFalse", "test.DNSCheckError",
             "test.DNSUpdateFalse"]],
        [pro.AddressProvider,
            ["test.Address", "test.AddressFalse", "test.AddressError"]],
        [pro.DNSProvider,
            ["test.DNS", "test.DNSCheckFalse", "test.DNSCheckError",
             "test.DNSUpdateFalse"]]
    ]
)
def test_list_providers(types, providers):
    assert list(pro.list_providers(types).keys()) == providers


def test_list_providers_invalid():
    with pt.raises(exc.InvalidProviderTypeError):
        pro.list_providers(int)


@pt.mark.parametrize(
    "name, base_type",
    [
        ["test.Address", pro.AddressProvider],
        ["test.DNS", pro.DNSProvider]
    ]
)
def test_get_provider(name, base_type):
    assert base_type in pro.get_provider(name).__bases__


def test_get_provider_unknown():
    with pt.raises(exc.NoSuchProviderError):
        pro.get_provider("test.unknown")
