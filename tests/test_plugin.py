import argparse as ap
import os
import updatemyip.plugin as plugin


def test_import_modules():
    modules = plugin.import_modules(*os.path.join(os.path.dirname(__file__), "plugins"))
    assert list(modules.keys()) == ["updatemyip_test"]


def test_list_address_plugins():
    assert plugin.list_plugins(plugin.PLUGIN_TYPE_ADDRESS) == ["test.address"]


def test_list_dns_plugins():
    assert plugin.list_plugins(plugin.PLUGIN_TYPE_DNS) == ["test.dns"]


def test_get_plugin():
    assert plugin.get_plugin("test.address")() == "test address plugin"


def test_list_plugin_options():
    assert list(plugin.list_plugin_options().keys()) == ["test.dns"]


def test_plugin_full_name():
    assert plugin._plugin_full_name("test_plugin") == "_pytest.python.test_plugin"


def test_strip_module_prefix():
    assert plugin._strip_module_prefix("updatemyip_test") == "test"
