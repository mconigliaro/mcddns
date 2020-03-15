import argparse as ap
import pytest as pt
import updatemyip.options as options


@pt.mark.parametrize(
    "args", [("foo",), ("bar", "--log-level", "debug"),],
)
def test_parse(args):
    assert isinstance(options.parse(args), ap.Namespace)
