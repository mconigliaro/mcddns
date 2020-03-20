import itertools as it
import logging as log
import updatemyip.options as opt
import updatemyip.plugin as pi
import updatemyip.util as util

RETURN_CODE_DRY_RUN = -2
RETURN_CODE_NOOP = -1
RETURN_CODE_SUCCESS = 0
RETURN_CODE_ERROR_ADDRESS = 1
RETURN_CODE_ERROR_DNS = 2


def main(plugin_module_paths=[], args=None):
    pi.import_modules(*plugin_module_paths)

    opts = opt.parse(args)

    address_plugins = {p: pi.init_plugin(p) for p in opts.address_plugin}
    plugins = it.product(range(opts.retry + 1), address_plugins.items())
    for attempt, (plugin_attempt, (plugin_name, plugin)) in enumerate(plugins):
        util.backoff(attempt, opts.no_backoff)
        counter = f"{plugin_attempt + 1}/{opts.retry + 1}"
        log.info(f"[{counter}] Trying address plugin: {plugin_name}")
        address = plugin.call("fetch", opts)
        if plugin.call("validate", opts, address):
            break
    else:
        log.error(f"All address plugins failed")
        return RETURN_CODE_ERROR_ADDRESS

    log.info(f"Got address: {address}")

    desired_record = f"{opts.fqdn} {opts.dns_ttl} {opts.dns_rrtype} {address}"
    plugin = pi.init_plugin(opts.dns_plugin)
    for attempt in range(opts.retry + 1):
        util.backoff(attempt, opts.no_backoff)
        counter = f"{attempt + 1}/{opts.retry + 1}"
        log.info(f"[{counter}] Trying DNS plugin: {opts.dns_plugin}")
        if plugin.call("check", opts, address):
            if opts.dry_run:
                log.info(f"DNS will be updated: {desired_record}")
                return RETURN_CODE_DRY_RUN
            else:
                if plugin.call("update", opts, address):
                    log.info(f"DNS updated: {desired_record}")
                    break
                else:
                    log.error(f"DNS update failed")
        else:
            log.info(f"No DNS update required")
            return RETURN_CODE_NOOP
    else:
        log.error(f"DNS plugin failed")
        return RETURN_CODE_ERROR_DNS

    return RETURN_CODE_SUCCESS
