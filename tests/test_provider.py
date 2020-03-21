import os
import pytest as pt
import updatemyip.exceptions as exc
import updatemyip.provider as pro


def test_import_modules():
    path = os.path.join(os.path.dirname(__file__), "providers")
    assert list(pro.import_modules(path).keys()) == ["updatemyip_test"]


@pt.mark.parametrize(
    "original, prefix, result",
    [
        [int, None, "builtins.int"],
        [int, "built", "ins.int"],
        [int, "otherprefix", "builtins.int"],
    ]
)
def test_provider_full_name(original, prefix, result):
    assert pro.provider_full_name(original, prefix) == result


@pt.mark.parametrize(
    "type, providers",
    [
        [pro.AddressProvider,
            ["test.Address", "test.AddressFalse", "test.AddressError"]],
        [pro.DNSProvider,
            ["test.DNS", "test.DNSCheckFalse", "test.DNSCheckError",
             "test.DNSUpdateFalse"]]
    ]
)
def test_list_providers(type, providers):
    assert list(pro.list_providers(type).keys()) == providers


@pt.mark.parametrize(
    "name, base_type",
    [
        ["test.Address", pro.AddressProvider],
        ["test.DNS", pro.DNSProvider]
    ]
)
def test_init_provider(name, base_type):
    assert base_type in pro.init_provider(name).__class__.__bases__


def test_init_provider_unknown():
    with pt.raises(exc.NoSuchProviderError):
        pro.init_provider("test.unknown")
