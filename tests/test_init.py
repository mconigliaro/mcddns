import pytest as pt
import os
import updatemyip as umip


@pt.mark.parametrize(
    "args, exit_code",
    [
        [
            "-a test.Address test.DNS test",
            umip.RETURN_CODE_SUCCESS
        ],
        [
            "-a test.AddressFalse --no-backoff test.DNS test",
            umip.RETURN_CODE_ERROR_ADDRESS
        ],
        [
            "-a test.AddressError --no-backoff test.DNS test",
            umip.RETURN_CODE_ERROR_ADDRESS
        ],
        [
            "-a test.Address --dry-run test.DNS test",
            umip.RETURN_CODE_DRY_RUN
        ],
        [
            "-a test.AddressFalse -a test.Address --no-backoff test.DNS test",
            umip.RETURN_CODE_SUCCESS
        ],
        [
            "-a test.Address --no-backoff test.DNSCheckFalse test --test",
            umip.RETURN_CODE_NOOP
        ],
        [
            "-a test.Address --no-backoff test.DNSCheckError test",
            umip.RETURN_CODE_ERROR_DNS
        ],
        [
            "-a test.Address --no-backoff test.DNSUpdateFalse test",
            umip.RETURN_CODE_ERROR_DNS
        ]
    ]
)
def test_main(args, exit_code):
    test_module_paths = [os.path.join(os.path.dirname(__file__), "providers")]
    assert umip.main(test_module_paths, args.split()) == exit_code
