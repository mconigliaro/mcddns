import updatemyip.plugin as plugin


@plugin.register_address_plugin(plugin.PLUGIN_RETURN_TYPE_IP_ADDRESS_PRIVATE)
def address(*args, **kwargs):
    return "127.0.0.1"


@plugin.register_dns_plugin()
def dns(*args, **kwargs):
    return plugin.PLUGIN_STATUS_SUCCESS


@plugin.register_plugin_options("dns")
def options(*args, **kwargs):
    return "test dns options"
