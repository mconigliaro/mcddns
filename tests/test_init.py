import pytest as pt
import os
import updatemyip as umip
import updatemyip.plugin as plugin


@pt.mark.parametrize(
    "args, exit_code",
    [
        [
            ["test", "-a", "test.address", "-d", "test.dns_noop"],
            plugin.PLUGIN_STATUS_NOOP
        ],
        [
            ["test", "-a", "test.address", "-d", "test.dns_dry_run",
             "--dry-run"],
            plugin.PLUGIN_STATUS_DRY_RUN
        ],
        [
            ["test", "-a", "test.address_fail", "-d", "test.dns",
             "--no-backoff"],
            plugin.PLUGIN_STATUS_FAILURE
        ],
        [
            ["test", "-a", "test.address_fail", "-a", "test.address",
             "-d", "test.dns", "--no-backoff"],
            plugin.PLUGIN_STATUS_SUCCESS
        ],
        [
            ["test", "-a", "test.address", "-d", "test.dns_fail",
             "--no-backoff"],
            plugin.PLUGIN_STATUS_FAILURE
        ],
        [
            ["test", "-a", "test.address", "-d", "test.dns"],
            plugin.PLUGIN_STATUS_SUCCESS
        ]
    ]
)
def test_main(args, exit_code):
    test_module_paths = [os.path.join(os.path.dirname(__file__), "plugins")]
    assert umip.main(test_module_paths, args) == exit_code
