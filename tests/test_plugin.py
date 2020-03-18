import os
import pytest as pt
import updatemyip.errors as errors
import updatemyip.plugin as plugin
import updatemyip.validator as validator


def test_import_modules():
    path = os.path.join(os.path.dirname(__file__), "plugins")
    assert list(plugin.import_modules(path).keys()) == ["updatemyip_test"]


@pt.mark.parametrize(
    "type, plugins",
    [
        [plugin.PLUGIN_TYPE_ADDRESS,
            ["test.address", "test.address_fail"]],
        [plugin.PLUGIN_TYPE_DNS,
            ["test.dns", "test.dns_noop", "test.dns_dry_run", "test.dns_fail"]]
    ]
)
def test_list_plugins(type, plugins):
    assert plugin.list_plugins(type) == plugins


def test_list_invalid_plugins():
    with pt.raises(errors.InvalidPluginTypeError):
        plugin.list_plugins(-1)


@pt.mark.parametrize(
    "name, type, validator_fn",
    [
        ["test.address", plugin.PLUGIN_TYPE_ADDRESS, validator.ipv4_address],
        ["test.dns", plugin.PLUGIN_TYPE_DNS, None]
    ]
)
def test_get_plugin(name, type, validator_fn):
    p = plugin.get_plugin(name)
    assert p["type"] == type
    if validator_fn:
        assert p["validator"] == validator_fn
    assert callable(p["function"])


def test_get_plugin_unknown():
    with pt.raises(errors.NoSuchPluginError):
        plugin.get_plugin("test.unknown")


def test_call_address_plugin():
    assert plugin.call_address_plugin("test.address") == "127.0.0.1"


def test_call_address_plugin_with_validation_error():
    with pt.raises(errors.ValidationError):
        plugin.call_address_plugin("test.address_fail")


def test_call_dns_plugin():
    assert plugin.call_dns_plugin("test.dns") == plugin.PLUGIN_STATUS_SUCCESS


def test_list_plugin_options():
    assert list(plugin.list_plugin_options().keys()) == ["test.dns"]
