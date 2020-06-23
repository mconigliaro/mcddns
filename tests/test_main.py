import pytest
import updatemyip
import updatemyip.options as options


@pytest.mark.parametrize(
    "args, exit_code",
    [
        [
            "test.DNS -a test.Address test",
            updatemyip.RETURN_CODE_DNS_UPDATED
        ],
        [
            "test.DNS -a test.AddressFalse --no-backoff test",
            updatemyip.RETURN_CODE_ADDRESS_ERROR
        ],
        [
            "test.DNS -a test.AddressError --no-backoff test",
            updatemyip.RETURN_CODE_ADDRESS_ERROR
        ],
        [
            "test.DNS -a test.Address --dry-run test",
            updatemyip.RETURN_CODE_DRY_RUN
        ],
        [
            "test.DNS -a test.AddressFalse -a test.Address --no-backoff test",
            updatemyip.RETURN_CODE_DNS_UPDATED
        ],
        [
            "test.DNSCheckFalse -a test.Address --no-backoff --test test",
            updatemyip.RETURN_CODE_DNS_NOOP
        ],
        [
            "test.DNSCheckError -a test.Address --no-backoff test",
            updatemyip.RETURN_CODE_DNS_ERROR
        ],
        [
            "test.DNSUpdateFalse -a test.Address --no-backoff test",
            updatemyip.RETURN_CODE_DNS_ERROR
        ]
    ]
)
def test_main(args, exit_code):
    opts = options.parse(args=args.split())
    assert updatemyip.main(opts) == exit_code


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


def test_state_read_none(test_state_none):
    assert not updatemyip.state_read(test_state_none)


def test_state_read(test_state_success):
    state = updatemyip.state_read(test_state_success)
    assert len(state) > 0


def test_state_write_none(test_state_none):
    data = "123"
    assert updatemyip.state_write(data, path=test_state_none)
    assert updatemyip.state_read(path=test_state_none) == data


def test_state_write(test_state_success):
    data = "456"
    assert updatemyip.state_write(data, path=test_state_success)
    assert updatemyip.state_read(path=test_state_success) == data


def test_state_remove_none(test_state_none):
    assert updatemyip.state_remove(test_state_none)


def test_state_remove_success(test_state_success):
    assert updatemyip.state_remove(test_state_success)
