import logging as log
import updatemyip.options as options
import updatemyip.plugin as plugin


def main():
    addr_plugins, dns_plugins = plugin.import_plugins(plugin.list_plugins())

    opts = options.parse(addr_plugins.keys(), dns_plugins.keys())
    opts_dict = vars(opts)

    log_format = "[%(levelname)s] %(message)s"
    log_level = getattr(log, opts.log_level.upper())
    log.basicConfig(format=log_format, level=log_level)

    log.debug(
        f"Discovered plugins: Address={','.join(addr_plugins.keys())} DNS={','.join(dns_plugins.keys())}"
    )

    log.debug(f"Options: {opts_dict}")

    addr_fn = getattr(addr_plugins[opts.addr_plugin], plugin.PLUGIN_ADDR_FN)
    log.debug(f"Calling {opts.addr_plugin}.{plugin.PLUGIN_ADDR_FN}()")
    addr = addr_fn(opts_dict)
    log.debug(f"Got address: {addr}")

    dns_fn = getattr(dns_plugins[opts.dns_plugin], plugin.PLUGIN_DNS_FN)
    log.debug(f"Calling {opts.dns_plugin}.{plugin.PLUGIN_DNS_FN}()")
    result = dns_fn(opts_dict, addr)

    if result == plugin.PLUGIN_NOOP:
        log.info(f"No changes required")
        exit_code = 0
    elif result == plugin.PLUGIN_SUCCESS:
        log.info(f"Changed {opts.fqdn} to {addr}")
        exit_code = 0
    elif result == plugin.PLUGIN_FAILURE:
        log.error(f"Update failed")
        exit_code = 1
    else:
        log.error(f"Plugin ({opts.dns_plugin}) status unknown: {result}")
        exit_code = 1

    return exit_code
