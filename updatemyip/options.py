import argparse as ap
import logging as log
import sys
import updatemyip.meta as meta
import updatemyip.provider as pi


def parse(args=None):
    address_providers = sorted(pi.list_providers(pi.AddressProvider).keys())
    dns_providers = sorted(pi.list_providers(pi.DNSProvider).keys())

    parser = ap.ArgumentParser(
        epilog=f"{meta.COPYRIGHT} ({meta.CONTACT})",
        formatter_class=ap.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument("fqdn", help="fully-qualified domain name")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what will happen without making changes"
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=10,
        help="timeout for network requests"
    )
    parser.add_argument(
        "--retry",
        type=int,
        default=2,
        help="number of times to retry failed providers"
    )
    parser.add_argument(
        "--no-backoff",
        action="store_true",
        help="disable Fibonacci backoff for failed providers"
    )
    parser.add_argument(
        "-l",
        "--log-level",
        choices=("debug", "info", "warning", "error", "critical"),
        default="info",
        help="show messages of this level or higher"
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{meta.NAME} {meta.VERSION}"
    )

    address_group = parser.add_argument_group("address provider arguments")
    address_group.add_argument(
        "-a",
        "--address-providers",
        choices=address_providers,
        default=[],
        action="append",
        required=True,
        help="provider(s) used to obtain an address"
    )

    dns_group = parser.add_argument_group("dns provider arguments")
    dns_group.add_argument(
        "-d",
        "--dns-provider",
        choices=dns_providers,
        required=True,
        help="provider used to manage DNS records"
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
        help="time in seconds for DNS servers to cache the record"
    )

    for name, cls in pi.list_providers().items():
        cls().options_pre(parser.add_argument_group(f"{name} arguments"))

    options = parser.parse_args(args)

    used_providers = options.address_providers + [options.dns_provider]
    post_parsers = [cls for name, cls in pi.list_providers().items()
                    if name in used_providers]
    for cls in post_parsers:
        cls().options_post(parser, options)

    if options.dry_run:
        log_format = "[%(levelname)s] (DRY-RUN) %(message)s"
    else:
        log_format = "[%(levelname)s] %(message)s"
    log_level = getattr(log, options.log_level.upper())
    log.basicConfig(format=log_format, level=log_level)

    log.debug(f"Provider search paths: {', '.join(sys.path)}")
    log.debug(f"Found address providers: {', '.join(address_providers)}")
    log.debug(f"Found DNS providers: {', '.join(dns_providers)}")
    options_str = ', '.join(f'{k}={repr(v)}'
                            for k, v in sorted(vars(options).items()))
    log.debug(f"Options: {options_str}")

    return options
