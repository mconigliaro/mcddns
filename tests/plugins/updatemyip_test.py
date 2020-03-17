import updatemyip.plugin as plugin
import updatemyip.validator as validator


@plugin.register_address_plugin(validator.ip_address_private)
def address(*args, **kwargs):
    return "127.0.0.1"


@plugin.register_dns_plugin()
def dns(*args, **kwargs):
    if "options" in kwargs: # FIXME: Shouldn't options always be sent?
        if kwargs["options"].fqdn.startswith("noop"):
            return plugin.PLUGIN_STATUS_NOOP
        elif kwargs["options"].dry_run:
            return plugin.PLUGIN_STATUS_DRY_RUN
        elif kwargs["options"].fqdn.startswith("fail"):
            return plugin.PLUGIN_STATUS_FAILURE

    return plugin.PLUGIN_STATUS_SUCCESS


@plugin.register_plugin_options("dns")
def options(*args, **kwargs):
    return "test dns options"
