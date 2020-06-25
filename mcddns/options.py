import argparse
import logging
import sys
import mcddns.meta as meta
import mcddns.provider as provider


log = logging.getLogger(__name__)


def parse(default_address_providers=[], args=None):
    addr_providers = provider.list_providers(provider.AddressProvider)
    addr_provider_names = sorted(addr_providers.keys())
    dns_providers = provider.list_providers(provider.DNSProvider)
    dns_provider_names = sorted(dns_providers.keys())

    parser = argparse.ArgumentParser(
        prog=meta.NAME,
        description=meta.DESCRIPTION,
        epilog=f"{meta.COPYRIGHT} ({meta.CONTACT})",
        # FIXME: https://bugs.python.org/issue27927
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{meta.NAME} {meta.VERSION}"
    )

    subparsers = parser.add_subparsers(help='dns providers')
    for dns_provider_name, dns_provider in dns_providers.items():
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
            choices=addr_provider_names,
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
            default=3,
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
            "--cron",
            action="store_true",
            help="use exit codes suitable for cron"
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
        dns_provider.options_pre(subparser)
        for addr_provider_name, addr_provider in addr_providers.items():
            addr_provider.options_pre(parser.add_argument_group(
                f"{addr_provider_name} arguments")
            )

    options = parser.parse_args(args)

    if not hasattr(options, "dns_provider"):
        parser.print_help()
        parser.exit(2)

    if not options.address_providers:
        options.address_providers = default_address_providers

    for name in options.address_providers + [options.dns_provider]:
        provider.get_provider(name)().options_post(parser, options)

    if options.dry_run:
        log_format = "[%(levelname)s] (DRY-RUN) %(message)s"
    else:
        log_format = "[%(levelname)s] %(message)s"
    log_level = getattr(logging, options.log_level.upper())
    logging.basicConfig(format=log_format, level=log_level)

    log.debug("Provider search paths: %s", ', '.join(sys.path))
    log.debug("Found address providers: %s", ', '.join(addr_provider_names))
    log.debug("Found DNS providers: %s", ', '.join(dns_provider_names))
    options_str = ', '.join(f'{k}={repr(v)}' for k, v in
                            sorted(vars(options).items()))
    log.debug("Options: %s", options_str)

    return options
