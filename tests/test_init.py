import pytest as pt
import os
import updatemyip as umip


@pt.mark.parametrize(
    "args, exit_code",
    [
        [
            ["test", "-a", "test.Address", "-d", "test.DNS"],
            umip.RETURN_CODE_SUCCESS
        ],
        [
            ["test", "-a", "test.AddressFail", "-d", "test.DNS",
             "--no-backoff"],
            umip.RETURN_CODE_ERROR_ADDRESS
        ],
        [
            ["test", "-a", "test.Address", "-d", "test.DNS", "--dry-run"],
            umip.RETURN_CODE_DRY_RUN
        ],
        [
            ["test", "-a", "test.AddressFail", "-a", "test.Address",
             "-d", "test.DNS", "--no-backoff"],
            umip.RETURN_CODE_SUCCESS
        ],
        [
            ["test", "-a", "test.Address", "-d", "test.DNSCheckFail",
             "--no-backoff"],
            umip.RETURN_CODE_NOOP
        ],
        [
            ["test", "-a", "test.Address", "-d", "test.DNSUpdateFail",
             "--no-backoff"],
            umip.RETURN_CODE_ERROR_DNS
        ]
    ]
)
def test_main(args, exit_code):
    test_module_paths = [os.path.join(os.path.dirname(__file__), "plugins")]
    assert umip.main(test_module_paths, args) == exit_code
