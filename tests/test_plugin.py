import os
import pytest as pt
import updatemyip.errors as errors
import updatemyip.plugin as plugin
import updatemyip.validator as validator


def test_import_modules():
    test_module_path = os.path.join(os.path.dirname(__file__), "plugins")
    modules = plugin.import_modules(test_module_path)
    assert list(modules.keys()) == ["updatemyip_test"]


@pt.mark.parametrize(
    "type, plugins",
    [
        [plugin.PLUGIN_TYPE_ADDRESS, ["test.address"]],
        [plugin.PLUGIN_TYPE_DNS, ["test.dns"]]
    ]
)
def test_list_plugins(type, plugins):
    assert plugin.list_plugins(type) == plugins


def test_list_invalid_plugins():
    with pt.raises(errors.InvalidPluginTypeError):
        plugin.list_plugins(-1)


def test_get_plugin():
    p = plugin.get_plugin("test.address")
    assert p["type"] == plugin.PLUGIN_TYPE_ADDRESS
    assert p["validator"] == validator.ipv4_address
    assert callable(p["function"])


def test_get_plugin_unknown():
    with pt.raises(errors.NoSuchPluginError):
        plugin.get_plugin("test.unknown")


def test_call_address_plugin():
    assert plugin.call_address_plugin("test.address") == "127.0.0.1"


def test_call_dns_plugin():
    assert plugin.call_dns_plugin("test.dns") == plugin.PLUGIN_STATUS_SUCCESS


def test_list_plugin_options():
    assert list(plugin.list_plugin_options().keys()) == ["test.dns"]
