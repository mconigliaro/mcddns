import logging as log
import updatemyip.options as options
import updatemyip.plugin as plugin


def main():
    modules = plugin.import_modules()
    address_plugins = plugin.list_plugins(plugin.PLUGIN_TYPE_ADDRESS)
    dns_plugins = plugin.list_plugins(plugin.PLUGIN_TYPE_DNS)

    options.parser.add_argument("fqdn")
    options.parser.add_argument(
        "--log-level",
        choices=("debug", "info", "warning", "error", "critical"),
        default="info",
    )

    address_group = options.parser.add_argument_group("address plugin arguments")
    address_group.add_argument(
        "-a", "--address-plugin", choices=address_plugins, default="ipify.ipv4",
    )

    dns_group = options.parser.add_argument_group("dns plugin arguments")
    dns_group.add_argument(
        "-d", "--dns-plugin", choices=dns_plugins, default="aws.route53",
    )
    dns_group.add_argument("--dns-rrtype", default="A")
    dns_group.add_argument("--dns-ttl", default=300)

    plugin.add_arguments(options.parser)

    opts = options.parser.parse_args(namespace=options.Options())

    log_format = "[%(levelname)s] %(message)s"
    log_level = getattr(log, opts.log_level.upper())
    log.basicConfig(format=log_format, level=log_level)

    log.debug(f"Modules: {', '.join(modules.keys())}")
    log.debug(f"Address plugins: {', '.join(address_plugins)}")
    log.debug(f"DNS plugins: {', '.join(dns_plugins)}")
    log.debug(f"Options: {options.log(opts)}")

    address = get_address(opts.address_plugin, opts)
    dns_result = update_dns(opts.dns_plugin, opts, address)

    return exit_status(dns_result, opts.fqdn, address)


def get_address(address_plugin, options):
    log.debug(f"Calling address plugin: {address_plugin}")
    address = plugin.get_plugin(address_plugin)(options=options)
    log.info(f"Got address: {address}")
    return address


def update_dns(dns_plugin, options, address):
    log.debug(f"Calling DNS plugin: {dns_plugin}")
    return plugin.get_plugin(dns_plugin)(options=options, address=address)


def exit_status(plugin_status, fqdn, address):
    if plugin_status == plugin.PLUGIN_STATUS_NOOP:
        log.info(f"No DNS update required")
        return 0
    elif plugin_status == plugin.PLUGIN_STATUS_SUCCESS:
        log.info(f"DNS updated: {fqdn} -> {address}")
        return 0
    elif plugin_status == plugin.PLUGIN_STATUS_FAILURE:
        log.error(f"DNS update failed")
        return 1
    else:
        log.error(f"DNS plugin returned unknown status: {plugin_status}")
        return 1
