import pytest as pt
import os
import updatemyip as umip
import updatemyip.plugin as pi


@pt.mark.parametrize(
    "args, exit_code",
    [
        [
            ["test", "-a", "test.Address", "-d", "test.DNSNoOp"],
            pi.PLUGIN_STATUS_NOOP
        ],
        [
            ["test", "-a", "test.Address", "-d", "test.DNSDryRun",
             "--dry-run"],
            pi.PLUGIN_STATUS_DRY_RUN
        ],
        [
            ["test", "-a", "test.AddressFail", "-d", "test.DNS",
             "--no-backoff"],
            pi.PLUGIN_STATUS_FAILURE
        ],
        [
            ["test", "-a", "test.AddressFail", "-a", "test.Address",
             "-d", "test.DNS", "--no-backoff"],
            pi.PLUGIN_STATUS_SUCCESS
        ],
        [
            ["test", "-a", "test.Address", "-d", "test.DNSFail",
             "--no-backoff"],
            pi.PLUGIN_STATUS_FAILURE
        ],
        [
            ["test", "-a", "test.Address", "-d", "test.DNS"],
            pi.PLUGIN_STATUS_SUCCESS
        ]
    ]
)
def test_main(args, exit_code):
    test_module_paths = [os.path.join(os.path.dirname(__file__), "plugins")]
    assert umip.main(test_module_paths, args) == exit_code
