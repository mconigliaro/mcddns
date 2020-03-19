import requests as req
import updatemyip.plugin as pi
import updatemyip.validator as val


class Ipv4(pi.AddressPlugin):

    def fetch(self, options):
        return req.get("https://api.ipify.org").text


class Ipv6(pi.AddressPlugin):

    def fetch(self, options):
        return req.get("https://api6.ipify.org").text

    def validate(self, options, address):
        return val.ip_address(address)
