import updatemyip.plugin as plugin
import updatemyip.validator as validator


@plugin.register_address_plugin(validator.ipv4_address)
def address(*args, **kwargs):
    return "127.0.0.1"


@plugin.register_address_plugin(validator.ipv4_address)
def address_fail(*args, **kwargs):
    return "fail"


@plugin.register_dns_plugin()
def dns(*args, **kwargs):
    return plugin.PLUGIN_STATUS_SUCCESS


@plugin.register_dns_plugin()
def dns_noop(*args, **kwargs):
    return plugin.PLUGIN_STATUS_NOOP


@plugin.register_dns_plugin()
def dns_dry_run(*args, **kwargs):
    return plugin.PLUGIN_STATUS_DRY_RUN


@plugin.register_dns_plugin()
def dns_fail(*args, **kwargs):
    return plugin.PLUGIN_STATUS_FAILURE


@plugin.register_plugin_options("dns")
def options(*args, **kwargs):
    return "test dns options"
