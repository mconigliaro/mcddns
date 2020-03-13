import logging as log
import updatemyip.options as options
import updatemyip.plugins as plugins


def main():
    addr_plugins, dns_plugins = plugins.import_plugins(plugins.list_plugins())

    opts = options.parse(addr_plugins.keys(), dns_plugins.keys())

    log_format = "[%(levelname)s] %(message)s"
    log_level = getattr(log, opts.log_level.upper())
    log.basicConfig(format=log_format, level=log_level)

    log.debug(
        f"Discovered plugins: Address={','.join(addr_plugins.keys())} DNS={','.join(dns_plugins.keys())}"
    )

    log.debug(f"Options: {opts}")

    addr_fn = getattr(addr_plugins[opts.addr_plugin], plugins.PLUGIN_ADDR_FN)
    log.debug(f"Calling {opts.addr_plugin}.{plugins.PLUGIN_ADDR_FN}()")
    addr = addr_fn(**vars(opts))
    log.debug(f"Got address: {addr}")

    dns_fn = getattr(dns_plugins[opts.dns_plugin], plugins.PLUGIN_DNS_FN)
    log.debug(f"Calling {opts.dns_plugin}.{plugins.PLUGIN_DNS_FN}()")
    dns_fn(**vars(opts))
