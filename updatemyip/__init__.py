import logging as log
import updatemyip.errors as errors
import updatemyip.options as options
import updatemyip.plugin as plugin


def main(plugin_module_paths=[], args=None):
    plugin.import_modules(*plugin_module_paths)

    opts = options.parse(args)

    for p in opts.address_plugin:
        log.debug(f"Calling address plugin: {p}")
        try:
            address = plugin.call_address_plugin(p, options=opts)
            break
        except errors.ValidationError as e:
            log.warn(e)
            next
    else:
        log.error(f"All address plugins failed")
        return 1

    log.debug(f"Calling DNS plugin: {opts.dns_plugin}")
    dns_result = plugin.call_dns_plugin(opts.dns_plugin, options=opts,
                                        address=address)

    desired_record = f"{opts.fqdn} {opts.dns_ttl} {opts.dns_rrtype} {address}"
    if dns_result == plugin.PLUGIN_STATUS_NOOP:
        log.info(f"No DNS update required")
        return 0
    elif dns_result == plugin.PLUGIN_STATUS_DRY_RUN:
        log.info(f"DNS will be updated: {desired_record}")
        return 0
    elif dns_result == plugin.PLUGIN_STATUS_SUCCESS:
        log.info(f"DNS updated: {desired_record}")
        return 0
    elif dns_result == plugin.PLUGIN_STATUS_FAILURE:
        log.error(f"DNS update failed")
        return 1
    else:
        log.error(f"DNS plugin returned unknown status: {dns_result}")
        return 1
