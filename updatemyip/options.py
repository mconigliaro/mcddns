import argparse as ap
import logging as log
import sys
import updatemyip.meta as meta
import updatemyip.plugin as plugin


def parse(args=None):
    address_plugins = plugin.list_plugins(plugin.PLUGIN_TYPE_ADDRESS)
    dns_plugins = plugin.list_plugins(plugin.PLUGIN_TYPE_DNS)

    parser = ap.ArgumentParser(epilog=f"{meta.COPYRIGHT} ({meta.CONTACT})")
    parser.add_argument(
        "-v", "--version", action="version", version=f"{meta.NAME} {meta.VERSION}"
    )

    parser.add_argument("fqdn", help="fully-qualified domain name")

    address_group = parser.add_argument_group("address plugin arguments")
    address_group.add_argument(
        "-a",
        "--address-plugin",
        choices=address_plugins,
        default="ipify.ipv4",
        help="plugin used to obtain an address",
    )

    dns_group = parser.add_argument_group("dns plugin arguments")
    dns_group.add_argument(
        "-d",
        "--dns-plugin",
        choices=dns_plugins,
        default="aws.route53",
        help="plugin used to manage DNS records",
    )
    dns_group.add_argument("--dns-rrtype", default="A", help="record type")
    dns_group.add_argument("--dns-ttl", type=int, default=300, help="time to live")

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="show what will happen without making changes",
    )
    parser.add_argument(
        "-l",
        "--log-level",
        choices=("debug", "info", "warning", "error", "critical"),
        default="info",
        help="show messages of this level or higher",
    )

    for name, fn in plugin.list_plugin_options().items():
        fn(parser=parser.add_argument_group(f"{name} arguments"))

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
    log.debug(
        f"Options: {', '.join(f'{k}={repr(v)}' for k, v in sorted(vars(options).items()))}"
    )

    return options
