import pytest
import updatemyip


@pytest.mark.parametrize(
    "args, exit_code",
    [
        [
            "test.DNS -a test.Address test",
            updatemyip.RETURN_CODE_SUCCESS
        ],
        [
            "test.DNS -a test.AddressFalse --no-backoff test",
            updatemyip.RETURN_CODE_ERROR_ADDRESS
        ],
        [
            "test.DNS -a test.AddressError --no-backoff test",
            updatemyip.RETURN_CODE_ERROR_ADDRESS
        ],
        [
            "test.DNS -a test.Address --dry-run test",
            updatemyip.RETURN_CODE_DRY_RUN
        ],
        [
            "test.DNS -a test.AddressFalse -a test.Address --no-backoff test",
            updatemyip.RETURN_CODE_SUCCESS
        ],
        [
            "test.DNSCheckFalse -a test.Address --no-backoff --test test",
            updatemyip.RETURN_CODE_NOOP
        ],
        [
            "test.DNSCheckError -a test.Address --no-backoff test",
            updatemyip.RETURN_CODE_ERROR_DNS
        ],
        [
            "test.DNSUpdateFalse -a test.Address --no-backoff test",
            updatemyip.RETURN_CODE_ERROR_DNS
        ]
    ]
)
def test_main(args, exit_code):
    assert updatemyip.main(args=args.split()) == exit_code


@pytest.mark.parametrize(
    "n, x",
    [
        [0, 1],
        [1, 1],
        [2, 2],
        [3, 3],
        [4, 5],
        [5, 8],
        [6, 13],
        [7, 21],
        [8, 34],
        [9, 55]
    ]
)
def test_fibonacci(n, x):
    assert updatemyip.fibonacci(n)[1] == x


def test_iterate_with_retry():
    iterable = "abc"
    tries = 3
    result = list(updatemyip.iterate_with_retry(
        iterable, tries=tries, no_backoff=True)
    )
    assert result == ["a", "b", "c", "a", "b", "c", "a", "b", "c"]
