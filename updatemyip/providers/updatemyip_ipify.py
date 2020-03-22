import updatemyip.provider as pro
import updatemyip.provider_util as pru


class IPv4(pro.AddressProvider):

    def fetch(self, options):
        return pru.fetch_url(
            "https://api.ipify.org/",
            timeout=options.timeout
        )


class IPv6(pro.AddressProvider):

    def fetch(self, options):
        return pru.fetch_url(
            "https://api6.ipify.org/",
            timeout=options.timeout
        )

    def validate(self, options, address):
        return pru.is_ip_address(address)
