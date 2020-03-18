import requests as req
import updatemyip.plugin as plugin
import updatemyip.validator as validator


@plugin.register_address_plugin(validator.ipv4_address)
def ipv4(options):
    return req.get("https://api.ipify.org").text


@plugin.register_address_plugin(validator.ip_address)
def ipv6(options):
    return req.get("https://api6.ipify.org").text
