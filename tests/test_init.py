import argparse as ap
import pytest as pt
import updatemyip as umip
import updatemyip.plugin as plugin


def test_get_address():
    assert umip.get_address(["test.address"], ap.Namespace) == "127.0.0.1"


def test_update_dns():
    assert (
        umip.update_dns("test.dns", ap.Namespace, "127.0.0.1")
        == plugin.PLUGIN_STATUS_SUCCESS
    )


@pt.mark.parametrize(
    "plugin_status, exit_code",
    [
        (plugin.PLUGIN_STATUS_NOOP, 0),
        (plugin.PLUGIN_STATUS_DRY_RUN, 0),
        (plugin.PLUGIN_STATUS_SUCCESS, 0),
        (plugin.PLUGIN_STATUS_FAILURE, 1),
        (-1, 1),
    ],
)
def test_exit_status(plugin_status, exit_code):
    opts = ap.Namespace(fqdn="localhost", dns_ttl=1, dns_rrtype="A")
    address = "127.0.0.1"
    assert umip.exit_status(plugin_status, opts, address) == exit_code
