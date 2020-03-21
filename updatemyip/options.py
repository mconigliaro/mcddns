import argparse as ap
import logging as log
import sys
import updatemyip.meta as meta
import updatemyip.provider as pro


def parse(args=None):
    address_providers = sorted(pro.list_providers(pro.AddressProvider).keys())
    dns_providers = sorted(pro.list_providers(pro.DNSProvider).keys())

    parser = ap.ArgumentParser(
        prog=meta.NAME,
        epilog=f"{meta.COPYRIGHT} ({meta.CONTACT})",
        formatter_class=ap.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-a",
        "--address-providers",
        choices=address_providers,
        default=[],
        action="append",
        help="provider(s) used to obtain an address"
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
        help="disable fibonacci backoff for failed providers"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what will happen without making changes"
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

    subparsers = parser.add_subparsers(help='dns provider')
    for name, cls in pro.list_providers().items():
        obj = cls()
        if isinstance(obj, pro.AddressProvider):
            obj.options_pre(parser.add_argument_group(f"{name} arguments"))
        elif isinstance(obj, pro.DNSProvider):
            subparser = subparsers.add_parser(
                name, help=f"use the {name} provider")
            subparser.add_argument("fqdn", help="fully-qualified domain name")
            subparser.add_argument(
                "--rrtype",
                default="A",
                help="record type"
            )
            subparser.add_argument(
                "--ttl",
                type=int,
                default=300,
                help="time to live"
            )
            subparser.set_defaults(dns_provider=name)
            obj.options_pre(subparser)

    options = parser.parse_args(args)

    used_providers = options.address_providers + [options.dns_provider]
    post_parsers = [cls for name, cls in pro.list_providers().items()
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
