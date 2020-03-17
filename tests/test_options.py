import pytest as pt
import updatemyip.options as options


@pt.mark.parametrize(
    "args", [
        ["foo.example.com"],
        ["bar.example.com", "--log-level", "debug"],
        ["baz.example.com", "--dry-run"]
    ],
)
def test_parse(args):
    assert options.parse(args).fqdn == args[0]
