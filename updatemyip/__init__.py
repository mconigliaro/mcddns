import itertools as it
import logging as log
import updatemyip.errors as errors
import updatemyip.options as options
import updatemyip.plugin as plugin
import updatemyip.util as util


def main(plugin_module_paths=[], args=None):
    plugin.import_modules(*plugin_module_paths)

    opts = options.parse(args)
    plugin_tries = opts.retry + 1

    addr_plugins = it.product(range(1, plugin_tries + 1), opts.address_plugin)
    for attempt, (plugin_attempt, p) in enumerate(addr_plugins):
        util.fibonacci_backoff(attempt, opts.no_backoff)
        counter = f"{plugin_attempt}/{plugin_tries}"
        log.debug(f"[{counter}] Calling address plugin: {p}")
        try:
            address = plugin.call_address_plugin(p, opts)
            break
        except errors.ValidationError as e:
            log.warning(e)
            next
    else:
        log.error(f"All address plugins failed")
        return plugin.PLUGIN_STATUS_FAILURE

    for attempt in range(plugin_tries):
        util.fibonacci_backoff(attempt, opts.no_backoff)
        counter = f"{attempt + 1}/{plugin_tries}"
        log.debug(f"[{counter}] Calling DNS plugin: {opts.dns_plugin}")
        dns_result = plugin.call_dns_plugin(opts.dns_plugin, opts, address)
        if dns_result in (plugin.PLUGIN_STATUS_NOOP,
                          plugin.PLUGIN_STATUS_DRY_RUN,
                          plugin.PLUGIN_STATUS_SUCCESS):
            break

    desired_record = f"{opts.fqdn} {opts.dns_ttl} {opts.dns_rrtype} {address}"
    if dns_result == plugin.PLUGIN_STATUS_NOOP:
        log.info(f"No DNS update required")
    elif dns_result == plugin.PLUGIN_STATUS_DRY_RUN:
        log.info(f"DNS will be updated: {desired_record}")
    elif dns_result == plugin.PLUGIN_STATUS_SUCCESS:
        log.info(f"DNS updated: {desired_record}")
    elif dns_result == plugin.PLUGIN_STATUS_FAILURE:
        log.error(f"DNS update failed")
    else:
        log.error(f"DNS plugin returned unknown status: {dns_result}")

    return dns_result
