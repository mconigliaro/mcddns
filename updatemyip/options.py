import argparse as ap

parser = ap.ArgumentParser()


class Options(ap.Namespace):
    pass


def parse(addr_plugins, dns_plugins, args=None):
    parser.add_argument("fqdn")
    parser.add_argument(
        "-a", "--addr-plugin", choices=addr_plugins, default="ipify",
    )
    parser.add_argument(
        "-d", "--dns-plugin", choices=dns_plugins, default="aws_route53",
    )
    parser.add_argument("--dns-rrtype", default="A")
    parser.add_argument("--dns-ttl", default=300)
    parser.add_argument(
        "--log-level",
        choices=("debug", "info", "warning", "error", "critical"),
        default="info",
    )

    return parser.parse_args(args, namespace=Options())
