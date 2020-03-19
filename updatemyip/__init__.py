import itertools as it
import logging as log
import updatemyip.options as opt
import updatemyip.plugin as pi
import updatemyip.util as util


def main(plugin_module_paths=[], args=None):
    pi.import_modules(*plugin_module_paths)

    opts = opt.parse(args)

    plugins = {p: pi.init_plugin(p) for p in opts.address_plugin}
    cycle = it.product(range(opts.retry + 1), plugins.keys(), plugins.values())
    for attempt, (plugin_attempt, plugin_name, plugin) in enumerate(cycle):
        util.backoff(attempt, opts.no_backoff)
        counter = f"{plugin_attempt + 1}/{opts.retry + 1}"
        log.debug(f"[{counter}] Trying address plugin: {plugin_name}")
        address = plugin.call("fetch", opts)
        if plugin.call("validate", opts, address):
            break
        else:
            next
    else:
        log.error(f"All address plugins failed")
        return pi.PLUGIN_STATUS_FAILURE

    log.info(f"Got address: {address}")

    plugin = pi.init_plugin(opts.dns_plugin)
    for attempt in range(opts.retry + 1):
        util.backoff(attempt, opts.no_backoff)
        counter = f"{attempt + 1}/{opts.retry + 1}"
        log.debug(f"[{counter}] Trying DNS plugin: {opts.dns_plugin}")
        dns_result = plugin.call("update", opts, address)
        if dns_result in (pi.PLUGIN_STATUS_NOOP,
                          pi.PLUGIN_STATUS_DRY_RUN,
                          pi.PLUGIN_STATUS_SUCCESS):
            break

    desired_record = f"{opts.fqdn} {opts.dns_ttl} {opts.dns_rrtype} {address}"
    if dns_result == pi.PLUGIN_STATUS_NOOP:
        log.info(f"No DNS update required")
    elif dns_result == pi.PLUGIN_STATUS_DRY_RUN:
        log.info(f"DNS will be updated: {desired_record}")
    elif dns_result == pi.PLUGIN_STATUS_SUCCESS:
        log.info(f"DNS updated: {desired_record}")
    elif dns_result == pi.PLUGIN_STATUS_FAILURE:
        log.error(f"DNS update failed")
    else:
        log.error(f"DNS plugin returned unknown status: {dns_result}")

    return dns_result
