import pytest as pt
import updatemyip as umip


@pt.mark.parametrize(
    "args, exit_code",
    [
        [
            "test.DNS -a test.Address test",
            umip.RETURN_CODE_SUCCESS
        ],
        [
            "test.DNS -a test.AddressFalse --no-backoff test",
            umip.RETURN_CODE_ERROR_ADDRESS
        ],
        [
            "test.DNS -a test.AddressError --no-backoff test",
            umip.RETURN_CODE_ERROR_ADDRESS
        ],
        [
            "test.DNS -a test.Address --dry-run test",
            umip.RETURN_CODE_DRY_RUN
        ],
        [
            "test.DNS -a test.AddressFalse -a test.Address --no-backoff test",
            umip.RETURN_CODE_SUCCESS
        ],
        [
            "test.DNSCheckFalse -a test.Address --no-backoff --test test",
            umip.RETURN_CODE_NOOP
        ],
        [
            "test.DNSCheckError -a test.Address --no-backoff test",
            umip.RETURN_CODE_ERROR_DNS
        ],
        [
            "test.DNSUpdateFalse -a test.Address --no-backoff test",
            umip.RETURN_CODE_ERROR_DNS
        ]
    ]
)
def test_main(args, exit_code):
    assert umip.main(args=args.split()) == exit_code
