import argparse as ap
import logging as log
import sys
import updatemyip.meta as meta
import updatemyip.provider as pro


def parse(default_address_providers=[], args=None):
    address_providers = pro.list_providers(pro.AddressProvider)
    address_provider_names = sorted(address_providers.keys())
    dns_providers = pro.list_providers(pro.DNSProvider)
    dns_provider_names = sorted(dns_providers.keys())

    parser = ap.ArgumentParser(
        prog=meta.NAME,
        epilog=f"{meta.COPYRIGHT} ({meta.CONTACT})",
        # FIXME: https://bugs.python.org/issue27927
        formatter_class=ap.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{meta.NAME} {meta.VERSION}"
    )

    subparsers = parser.add_subparsers(help='dns providers')
    for dns_provider_name, dns_provider_cls in dns_providers.items():
        subparser = subparsers.add_parser(
            dns_provider_name,
            help=f"use the {dns_provider_name} provider"
        )
        subparser.add_argument(
            "fqdn",
            help="fully-qualified domain name"
        )
        subparser.add_argument(
            "-a",
            "--address-providers",
            choices=address_provider_names,
            default=[],
            action="append",
            help="provider(s) used to obtain an address"
        )
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
        subparser.add_argument(
            "--timeout",
            type=float,
            default=15,
            help="timeout for network requests"
        )
        subparser.add_argument(
            "--retry",
            type=int,
            default=2,
            help="number of times to retry failed providers"
        )
        subparser.add_argument(
            "--no-backoff",
            action="store_true",
            help="disable fibonacci backoff for failed providers"
        )
        subparser.add_argument(
            "--dry-run",
            action="store_true",
            help="show what will happen without making changes"
        )
        subparser.add_argument(
            "-l",
            "--log-level",
            choices=("debug", "info", "warning", "error", "critical"),
            default="info",
            help="show messages of this level or higher"
        )

        subparser.set_defaults(dns_provider=dns_provider_name)
        dns_provider_cls().options_pre(subparser)
        for addr_provider_name, addr_provider_cls in address_providers.items():
            addr_provider_cls().options_pre(parser.add_argument_group(
                f"{addr_provider_name} arguments")
            )

    options = parser.parse_args(args)

    if not hasattr(options, "dns_provider"):
        parser.print_help()
        parser.exit(2)

    if not options.address_providers:
        options.address_providers = default_address_providers

    for name in options.address_providers + [options.dns_provider]:
        pro.get_provider(name)().options_post(parser, options)

    if options.dry_run:
        log_format = "[%(levelname)s] (DRY-RUN) %(message)s"
    else:
        log_format = "[%(levelname)s] %(message)s"
    log_level = getattr(log, options.log_level.upper())
    log.basicConfig(format=log_format, level=log_level)

    log.debug(f"Provider search paths: {', '.join(sys.path)}")
    log.debug(f"Found address providers: {', '.join(address_provider_names)}")
    log.debug(f"Found DNS providers: {', '.join(dns_provider_names)}")
    options_str = ', '.join(f'{k}={repr(v)}'
                            for k, v in sorted(vars(options).items()))
    log.debug(f"Options: {options_str}")

    return options
