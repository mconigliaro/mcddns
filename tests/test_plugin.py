import os
import pytest as pt
import updatemyip.errors as errors
import updatemyip.plugin as plugin


def test_import_modules():
    path = os.path.join(os.path.dirname(__file__), "plugins")
    assert list(plugin.import_modules(path).keys()) == ["updatemyip_test"]


@pt.mark.parametrize(
    "type, plugins",
    [
        [plugin.AddressPlugin,
            ["test.Address", "test.AddressFail"]],
        [plugin.DNSPlugin,
            ["test.DNS", "test.DNSNoOp", "test.DNSDryRun", "test.DNSFail"]]
    ]
)
def test_list_plugins(type, plugins):
    assert list(plugin.list_plugins(type).keys()) == plugins


@pt.mark.parametrize(
    "name, base_type",
    [
        ["test.Address", plugin.AddressPlugin],
        ["test.DNS", plugin.DNSPlugin]
    ]
)
def test_get_plugin(name, base_type):
    assert base_type in plugin.get_plugin(name).__bases__


def test_get_plugin_unknown():
    with pt.raises(errors.NoSuchPluginError):
        plugin.get_plugin("test.unknown")
