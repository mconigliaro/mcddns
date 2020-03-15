import logging as log
import os
import updatemyip.options as options
import updatemyip.plugin as plugin


def main():
    builtin_plugins = os.path.join(os.path.dirname(__file__), "plugins")
    plugin.import_modules(builtin_plugins)

    opts = options.parse()
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
