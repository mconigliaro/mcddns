import argparse as ap
import os
import pytest as pt
import updatemyip.errors as errors
import updatemyip.plugin as plugin


def test_import_modules():
    test_module_path = os.path.join(os.path.dirname(__file__), "plugins")
    modules = plugin.import_modules(*test_module_path)
    assert list(modules.keys()) == ["updatemyip_test"]


def test_plugin_full_name():
    assert plugin.plugin_full_name("test_plugin") == "_pytest.python.test_plugin"


def test_strip_module_prefix():
    assert plugin.strip_module_prefix("updatemyip_test") == "test"
    assert plugin.strip_module_prefix("otherprefix_test") == "otherprefix_test"


def test_register_address_plugin_failure():
    with pt.raises(errors.InvalidPluginReturnTypeError):

        @plugin.register_address_plugin(-1)
        def address(*args, **kwargs):
            return "127.0.0.1"


def test_list_address_plugins():
    assert plugin.list_plugins(plugin.PLUGIN_TYPE_ADDRESS) == ["test.address"]


def test_list_dns_plugins():
    assert plugin.list_plugins(plugin.PLUGIN_TYPE_DNS) == ["test.dns"]


def test_list_invalid_plugins():
    with pt.raises(errors.InvalidPluginTypeError):
        plugin.list_plugins(-1)


def test_get_plugin():
    p = plugin.get_plugin("test.address")
    assert p["plugin_type"] == plugin.PLUGIN_TYPE_ADDRESS
    assert p["return_type"] == plugin.PLUGIN_RETURN_TYPE_IP_ADDRESS_PRIVATE
    assert callable(p["function"])


def test_get_plugin_unknown():
    with pt.raises(errors.NoSuchPluginError):
        plugin.get_plugin("test.unknown")


def test_call_address_plugin_function():
    assert plugin.call_address_plugin_function("test.address") == "127.0.0.1"


def test_call_dns_plugin_function():
    assert plugin.call_dns_plugin_function("test.dns") == plugin.PLUGIN_STATUS_SUCCESS


def test_to_ip_address():
    assert str(plugin.to_ip_address("127.0.0.1")) == "127.0.0.1"


def test_to_ip_address_failure():
    with pt.raises(errors.DataValidationError):
        plugin.to_ip_address("test")


def test_is_ip_address_private():
    assert plugin.is_ip_address_private("127.0.0.1")


def test_is_ip_address_private_failure():
    with pt.raises(errors.DataValidationError):
        plugin.is_ip_address_private("1.1.1.1")


def test_is_ip_address_global():
    assert plugin.is_ip_address_global("1.1.1.1")


def test_is_ip_address_global_failure():
    with pt.raises(errors.DataValidationError):
        plugin.is_ip_address_global("127.0.0.1")


def test_is_hostname():
    assert plugin.is_hostname("localhost")


def test_is_hostname_failure():
    with pt.raises(errors.DataValidationError):
        plugin.is_hostname("foo.bar")


def test_list_plugin_options():
    assert list(plugin.list_plugin_options().keys()) == ["test.dns"]
