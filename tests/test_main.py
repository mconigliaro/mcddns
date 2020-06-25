import pytest
import mcddns
import mcddns.options as options


@pytest.mark.parametrize(
    "args, exit_code",
    [
        [
            "test.DNS -a test.Address test",
            mcddns.RETURN_CODE_DNS_UPDATED
        ],
        [
            "test.DNS -a test.AddressFalse --no-backoff test",
            mcddns.RETURN_CODE_ADDRESS_ERROR
        ],
        [
            "test.DNS -a test.AddressError --no-backoff test",
            mcddns.RETURN_CODE_ADDRESS_ERROR
        ],
        [
            "test.DNS -a test.Address --dry-run test",
            mcddns.RETURN_CODE_DRY_RUN
        ],
        [
            "test.DNS -a test.AddressFalse -a test.Address --no-backoff test",
            mcddns.RETURN_CODE_DNS_UPDATED
        ],
        [
            "test.DNSCheckFalse -a test.Address --no-backoff --test test",
            mcddns.RETURN_CODE_DNS_NOOP
        ],
        [
            "test.DNSCheckError -a test.Address --no-backoff test",
            mcddns.RETURN_CODE_DNS_ERROR
        ],
        [
            "test.DNSUpdateFalse -a test.Address --no-backoff test",
            mcddns.RETURN_CODE_DNS_ERROR
        ]
    ]
)
def test_main(args, exit_code):
    opts = options.parse(args=args.split())
    assert mcddns.main(opts) == exit_code


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
    assert mcddns.fibonacci(n)[1] == x


def test_iterate_with_retry():
    iterable = "abc"
    tries = 3
    result = list(mcddns.iterate_with_retry(
        iterable, tries=tries, no_backoff=True)
    )
    assert result == ["a", "b", "c", "a", "b", "c", "a", "b", "c"]


def test_state_read_missing(test_state):
    mcddns.state_remove(path=test_state)
    assert not mcddns.state_read(test_state)


def test_state_read(test_state):
    state = mcddns.state_read(test_state)
    assert state == ""


def test_state_write_missing(test_state):
    mcddns.state_remove(path=test_state)
    data = "123"
    mcddns.state_write(data, path=test_state)
    assert mcddns.state_read(path=test_state) == data


def test_state_write(test_state):
    data = "456"
    mcddns.state_write(data, path=test_state)
    assert mcddns.state_read(path=test_state) == data


def test_state_remove_missing(test_state):
    mcddns.state_remove(path=test_state)
    assert mcddns.state_remove(test_state)


def test_state_remove(test_state):
    assert mcddns.state_remove(test_state)


@pytest.mark.parametrize(
    "rc, rc_class",
    [
        ["", None],
        [100, 1],
    ]
)
def test_return_code_class(rc, rc_class):
    assert mcddns.return_code_class(rc) == rc_class


@pytest.mark.parametrize(
    "rc1, rc2, transition",
    [
        [100, 200, (1, 2)],
        [300, 400, (3, 4)]
    ]
)
def test_return_code_class_transition(rc1, rc2, transition):
    assert mcddns.return_code_class_transition(rc1, rc2) == transition


@pytest.mark.parametrize(
    "return_codes, cron, exit_code",
    [
        [("", 100), False, 0],
        [("", 200), False, 0],
        [("", 300), False, 1],

        [("", 100), True, 0],
        [("", 200), True, 1],
        [("", 300), True, 1],
        [(100, 100), True, 0],
        [(100, 200), True, 1],
        [(100, 300), True, 1],
        [(200, 100), True, 0],
        [(200, 200), True, 1],
        [(200, 300), True, 1],
        [(300, 100), True, 1],
        [(300, 200), True, 1],
        [(300, 300), True, 0]
    ]
)
def test_exit_code(return_codes, cron, test_state, exit_code):
    mcddns.state_write(return_codes[0], path=test_state)
    assert mcddns.exit_code(return_codes[1], cron, test_state) == exit_code
