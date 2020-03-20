import requests as req
import updatemyip.errors as err
import updatemyip.plugin as pi
import updatemyip.validator as val


class Ipv4(pi.AddressPlugin):

    def fetch(self, options):
        try:
            return req.get("https://api.ipify.org",
                           timeout=options.timeout).text
        except req.exceptions.Timeout as e:
            raise err.PluginError(e)


class Ipv6(pi.AddressPlugin):

    def fetch(self, options):
        try:
            return req.get("https://api6.ipify.org",
                           timeout=options.timeout).text
        except req.exceptions.Timeout as e:
            raise err.PluginError(e)

    def validate(self, options, address):
        return val.ip_address(address)
