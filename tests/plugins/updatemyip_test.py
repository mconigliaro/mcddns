import updatemyip.plugin as plugin


@plugin.register_plugin(plugin.PLUGIN_TYPE_ADDRESS)
def address(*args, **kwargs):
    return "test address plugin"


@plugin.register_plugin(plugin.PLUGIN_TYPE_DNS)
def dns(*args, **kwargs):
    return "test dns plugin"


@plugin.register_plugin_options("dns")
def options(*args, **kwargs):
    return "test dns options"
