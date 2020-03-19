import itertools as it
import logging as log
import updatemyip.errors as err
import updatemyip.options as opt
import updatemyip.plugin as pi
import updatemyip.util as util


def main(plugin_module_paths=[], args=None):
    pi.import_modules(*plugin_module_paths)

    opts = opt.parse(args)
    plugin_tries = opts.retry + 1

    addr_plugins = it.product(range(1, plugin_tries + 1), opts.address_plugin)
    for attempt, (plugin_attempt, p) in enumerate(addr_plugins):
        util.backoff(attempt, opts.no_backoff)
        counter = f"{plugin_attempt}/{plugin_tries}"
        log.debug(f"[{counter}] Calling address plugin: {p}")
        try:
            address = pi.get_plugin(p)().fetch(opts)
            log.info(f"Got address: {address}")
            log.debug(f"Validating address: {address}")
            if not pi.get_plugin(p)().validate(opts, address):
                raise err.ValidationError(f"Address validation failed")
            break
        except err.ValidationError as e:
            log.warning(e)
            next
    else:
        log.error(f"All address plugins failed")
        return pi.PLUGIN_STATUS_FAILURE

    for attempt in range(plugin_tries):
        util.backoff(attempt, opts.no_backoff)
        counter = f"{attempt + 1}/{plugin_tries}"
        log.debug(f"[{counter}] Calling DNS plugin: {opts.dns_plugin}")
        dns_result = pi.get_plugin(opts.dns_plugin)().update(opts, address)
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
