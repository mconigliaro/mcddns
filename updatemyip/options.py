import argparse as ap
import logging as log
import updatemyip.plugin as plugin


def parse(args=None):
    address_plugins = plugin.list_plugins(plugin.PLUGIN_TYPE_ADDRESS)
    dns_plugins = plugin.list_plugins(plugin.PLUGIN_TYPE_DNS)

    parser = ap.ArgumentParser()

    parser.add_argument("fqdn")

    parser.add_argument(
        "--log-level",
        choices=("debug", "info", "warning", "error", "critical"),
        default="info",
    )

    address_group = parser.add_argument_group("address plugin arguments")
    address_group.add_argument(
        "-a", "--address-plugin", choices=address_plugins, default="ipify.ipv4",
    )

    dns_group = parser.add_argument_group("dns plugin arguments")
    dns_group.add_argument(
        "-d", "--dns-plugin", choices=dns_plugins, default="aws.route53",
    )
    dns_group.add_argument("--dns-rrtype", default="A")
    dns_group.add_argument("--dns-ttl", default=300)

    plugin.add_options(parser)

    options = parser.parse_args(args)

    log_format = "[%(levelname)s] %(message)s"
    log_level = getattr(log, options.log_level.upper())
    log.basicConfig(format=log_format, level=log_level)

    log.debug(f"Address plugins: {', '.join(address_plugins)}")
    log.debug(f"DNS plugins: {', '.join(dns_plugins)}")
    log.debug(
        f"Options: {', '.join(f'{k}={repr(v)}' for k, v in sorted(vars(options).items()))}"
    )

    return options
