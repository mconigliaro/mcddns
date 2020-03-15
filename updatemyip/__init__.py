import logging as log
import updatemyip.options as options
import updatemyip.plugin as plugin


def main():
    plugin.import_modules(*plugin.PLUGIN_MODULE_PATHS)

    opts = options.parse()
    address = get_address(opts.address_plugin, opts)
    dns_result = update_dns(opts.dns_plugin, opts, address)

    return exit_status(dns_result, opts, address)


def get_address(address_plugin, opts):
    log.debug(f"Calling address plugin: {address_plugin}")
    address = plugin.get_plugin(address_plugin)(options=opts)
    log.info(f"Got address: {address}")
    return address


def update_dns(dns_plugin, opts, address):
    log.debug(f"Calling DNS plugin: {dns_plugin}")
    return plugin.get_plugin(dns_plugin)(options=opts, address=address)


def exit_status(plugin_status, opts, address):
    desired_record = f"{opts.fqdn} {opts.dns_ttl} {opts.dns_rrtype} {address}"
    if plugin_status == plugin.PLUGIN_STATUS_NOOP:
        log.info(f"No DNS update required")
        return 0
    elif plugin_status == plugin.PLUGIN_STATUS_DRY_RUN:
        log.info(f"DNS will be updated: {desired_record}")
        return 0
    elif plugin_status == plugin.PLUGIN_STATUS_SUCCESS:
        log.info(f"DNS updated: {desired_record}")
        return 0
    elif plugin_status == plugin.PLUGIN_STATUS_FAILURE:
        log.error(f"DNS update failed")
        return 1
    else:
        log.error(f"DNS plugin returned unknown status: {plugin_status}")
        return 1
