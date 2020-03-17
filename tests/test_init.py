import pytest as pt
import os
import updatemyip as umip


@pt.mark.parametrize(
    "args, exit_code",
    [
        [["noop.example.com", "--no-backoff"], 0],
        [["example.com", "--no-backoff"], 0],
        [["fail.example.com", "--no-backoff"], 1],
        [["example.com", "--no-backoff"], 0],
    ],
)
def test_main(args, exit_code):
    test_module_paths = [os.path.join(os.path.dirname(__file__), "plugins")]
    assert umip.main(test_module_paths, args) == exit_code
