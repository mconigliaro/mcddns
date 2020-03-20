import argparse as ap
import logging as log
import sys
import updatemyip.meta as meta
import updatemyip.plugin as pi


def parse(args=None):
    address_plugins = sorted(pi.list_plugins(pi.AddressPlugin).keys())
    dns_plugins = sorted(pi.list_plugins(pi.DNSPlugin).keys())

    parser = ap.ArgumentParser(epilog=f"{meta.COPYRIGHT} ({meta.CONTACT})")

    parser.add_argument("fqdn", help="fully-qualified domain name")

    address_group = parser.add_argument_group("address plugin arguments")
    address_group.add_argument(
        "-a",
        "--address-plugin",
        choices=address_plugins,
        default=[],
        action="append",
        required=True,
        help="plugin(s) used to obtain an address",
    )

    dns_group = parser.add_argument_group("dns plugin arguments")
    dns_group.add_argument(
        "-d",
        "--dns-plugin",
        choices=dns_plugins,
        required=True,
        help="plugin used to manage DNS records",
    )
    dns_group.add_argument(
        "--dns-rrtype",
        default="A",
        help="type of DNS record"
    )
    dns_group.add_argument(
        "--dns-ttl",
        type=int,
        default=300,
        help="time in seconds that DNS servers should cache the record"
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what will happen without making changes",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10,
        help="timeout for network requests",
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=2,
        help="number of times to retry failed plugins",
    )
    parser.add_argument(
        "--no-backoff",
        action="store_false",
        help="disable Fibonacci backoff for failed plugins",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        choices=("debug", "info", "warning", "error", "critical"),
        default="info",
        help="show messages of this level or higher",
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{meta.NAME} {meta.VERSION}"
    )

    for name, cls in pi.list_plugins().items():
        cls().options(parser.add_argument_group(f"{name} arguments"))

    options = parser.parse_args(args)

    if options.dry_run:
        log_format = "[%(levelname)s] (DRY-RUN) %(message)s"
    else:
        log_format = "[%(levelname)s] %(message)s"
    log_level = getattr(log, options.log_level.upper())
    log.basicConfig(format=log_format, level=log_level)

    log.debug(f"Plugin search paths: {', '.join(sys.path)}")
    log.debug(f"Found address plugins: {', '.join(address_plugins)}")
    log.debug(f"Found DNS plugins: {', '.join(dns_plugins)}")
    options_str = ', '.join(f'{k}={repr(v)}'
                            for k, v in sorted(vars(options).items()))
    log.debug(f"Options: {options_str}")

    return options
