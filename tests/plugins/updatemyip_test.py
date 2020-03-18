import updatemyip.plugin as plugin
import updatemyip.validator as validator


@plugin.register_address_plugin(validator.ipv4_address)
def address(options):
    return "127.0.0.1"


@plugin.register_address_plugin(validator.ipv4_address)
def address_fail(options):
    return "fail"


@plugin.register_plugin_options("dns")
def dns_options(parser):
    return "test dns options"


@plugin.register_dns_plugin()
def dns(options, address):
    return plugin.PLUGIN_STATUS_SUCCESS


@plugin.register_dns_plugin()
def dns_noop(options, address):
    return plugin.PLUGIN_STATUS_NOOP


@plugin.register_dns_plugin()
def dns_dry_run(options, address):
    return plugin.PLUGIN_STATUS_DRY_RUN


@plugin.register_dns_plugin()
def dns_fail(options, address):
    return plugin.PLUGIN_STATUS_FAILURE
