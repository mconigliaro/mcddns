import argparse as ap

parser = ap.ArgumentParser()


class Options(ap.Namespace):
    pass


def parse(addr_plugins, dns_plugins, args=None):

    parser.add_argument(
        "-a", "--addr-plugin", choices=addr_plugins, default="ipify",
    )
    parser.add_argument("--addr-timeout", default=30)

    parser.add_argument(
        "-d", "--dns-plugin", choices=dns_plugins, default="aws_route53",
    )
    parser.add_argument("--dns-timeout", default=30)

    parser.add_argument(
        "--log-level",
        choices=("debug", "info", "warning", "error", "critical"),
        default="info",
    )

    return parser.parse_args(args, namespace=Options())
