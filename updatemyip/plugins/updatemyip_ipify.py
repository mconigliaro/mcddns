import requests as req
import updatemyip.plugin as plugin


@plugin.register_address_plugin(plugin.PLUGIN_RETURN_TYPE_IP_ADDRESS_GLOBAL)
def ipv4(*args, **kwargs):
    return req.get("https://api.ipify.org").text


@plugin.register_address_plugin(plugin.PLUGIN_RETURN_TYPE_IP_ADDRESS_GLOBAL)
def ipv6(*args, **kwargs):
    return req.get("https://api6.ipify.org").text
