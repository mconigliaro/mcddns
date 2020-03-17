import os
import pytest as pt
import updatemyip.errors as errors
import updatemyip.plugin as plugin


def test_import_modules():
    test_module_path = os.path.join(os.path.dirname(__file__), "plugins")
    modules = plugin.import_modules(test_module_path)
    assert list(modules.keys()) == ["updatemyip_test"]


def test_plugin_full_name():
    assert plugin.plugin_full_name("test_plugin") == "_pytest.python.test_plugin"


@pt.mark.parametrize(
    "original, stripped",
    [
        ["updatemyip_test", "test"],
        ["otherprefix_test", "otherprefix_test"]
    ]
)
def test_strip_module_prefix(original, stripped):
    assert plugin.strip_module_prefix(original) == stripped


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
    assert p["validator"] == plugin.is_ip_address_private
    assert callable(p["function"])


def test_get_plugin_unknown():
    with pt.raises(errors.NoSuchPluginError):
        plugin.get_plugin("test.unknown")


def test_call_address_plugin():
    assert plugin.call_address_plugin("test.address") == "127.0.0.1"


def test_call_dns_plugin():
    assert plugin.call_dns_plugin("test.dns") == plugin.PLUGIN_STATUS_SUCCESS


@pt.mark.parametrize(
    "value, result",
    [
        ["127.0.0.1", True],
        ["test", False]
    ]
)
def test_is_ip_address(value, result):
    assert plugin.is_ip_address(value) == result


@pt.mark.parametrize(
    "value, result",
    [
        ["127.0.0.1", True],
        ["1.1.1.1", False]
    ]
)
def test_is_ip_address_private(value, result):
    assert plugin.is_ip_address_private(value) == result


@pt.mark.parametrize(
    "value, result",
    [
        ["1.1.1.1", True],
        ["127.0.0.1", False]
    ]
)
def test_is_ip_address_global(value, result):
    assert plugin.is_ip_address_global(value) == result


@pt.mark.parametrize(
    "value, result",
    [
        ["foo.bar", True],
        ["fail!", False]
    ]
)
def test_is_hostname(value, result):
    assert plugin.is_hostname(value) == result


def test_list_plugin_options():
    assert list(plugin.list_plugin_options().keys()) == ["test.dns"]
