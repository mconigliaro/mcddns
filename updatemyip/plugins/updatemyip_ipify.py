import requests as req
import updatemyip.plugin as plugin


class Ipv4(plugin.AddressPlugin):

    def fetch(self, options):
        return req.get("https://api.ipify.org").text


class Ipv6(plugin.AddressPlugin):

    def fetch(self, options):
        return req.get("https://api6.ipify.org").text
