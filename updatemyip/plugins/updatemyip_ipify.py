import requests as req
import updatemyip.plugin as plugin


@plugin.register_address_plugin(plugin.is_ip_address_global)
def ipv4(*args, **kwargs):
    return req.get("https://api.ipify.org").text


@plugin.register_address_plugin(plugin.is_ip_address_global)
def ipv6(*args, **kwargs):
    return req.get("https://api6.ipify.org").text
