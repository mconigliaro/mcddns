import os
import pytest as pt
import updatemyip.errors as err
import updatemyip.plugin as pi


def test_import_modules():
    path = os.path.join(os.path.dirname(__file__), "plugins")
    assert list(pi.import_modules(path).keys()) == ["updatemyip_test"]


@pt.mark.parametrize(
    "type, plugins",
    [
        [pi.AddressPlugin,
            ["test.Address", "test.AddressFail"]],
        [pi.DNSPlugin,
            ["test.DNS", "test.DNSNoOp", "test.DNSDryRun", "test.DNSFail"]]
    ]
)
def test_list_plugins(type, plugins):
    assert list(pi.list_plugins(type).keys()) == plugins


@pt.mark.parametrize(
    "name, base_type",
    [
        ["test.Address", pi.AddressPlugin],
        ["test.DNS", pi.DNSPlugin]
    ]
)
def test_get_plugin(name, base_type):
    assert base_type in pi.get_plugin(name).__bases__


def test_get_plugin_unknown():
    with pt.raises(err.NoSuchPluginError):
        pi.get_plugin("test.unknown")
