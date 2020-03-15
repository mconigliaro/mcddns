import requests as req
import updatemyip.plugin as plugin


@plugin.register_plugin(plugin.PLUGIN_TYPE_ADDRESS)
def ipv4(**kwargs):
    return req.get("https://api.ipify.org").text


@plugin.register_plugin(plugin.PLUGIN_TYPE_ADDRESS)
def ipv6(**kwargs):
    return req.get("https://api6.ipify.org").text
