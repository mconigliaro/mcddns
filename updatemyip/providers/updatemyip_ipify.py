import updatemyip.provider as pro
import updatemyip.validator as val


class IPv4(pro.AddressProvider):

    def fetch(self, options):
        return self._fetch_url(options, "https://api.ipify.org/")


class IPv6(pro.AddressProvider):

    def fetch(self, options):
        return self._fetch_url(options, "https://api6.ipify.org/")

    def validate(self, options, address):
        return val.ip_address(address)
