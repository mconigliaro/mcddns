import pytest as pt
import os
import updatemyip as umip
import updatemyip.plugin as plugin


@pt.mark.parametrize(
    "args, exit_code",
    [
        [
            ["noop.example.com", "--no-backoff"],
            plugin.PLUGIN_STATUS_NOOP
        ],
        [
            ["dry-run.example.com", "--no-backoff", "--dry-run"],
            plugin.PLUGIN_STATUS_DRY_RUN
        ],
        [
            ["fail.example.com", "--no-backoff"],
            plugin.PLUGIN_STATUS_FAILURE
        ],
        [
            ["example.com", "--no-backoff"],
            plugin.PLUGIN_STATUS_SUCCESS
        ]
    ]
)
def test_main(args, exit_code):
    test_module_paths = [os.path.join(os.path.dirname(__file__), "plugins")]
    assert umip.main(test_module_paths, args) == exit_code
