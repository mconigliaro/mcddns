import requests as req
import updatemyip.exceptions as exc
import updatemyip.plugin as pi
import updatemyip.validator as val


class Ipv4(pi.AddressPlugin):

    def fetch(self, options):
        try:
            return req.get("https://api.ipify.org",
                           timeout=options.timeout).text
        except req.exceptions.RequestException as e:
            raise exc.PluginError(e) from e


class Ipv6(pi.AddressPlugin):

    def fetch(self, options):
        try:
            return req.get("https://api6.ipify.org",
                           timeout=options.timeout).text
        except req.exceptions.RequestException as e:
            raise exc.PluginError(e) from e

    def validate(self, options, address):
        return val.ip_address(address)
