import updatemyip.provider as pro
import updatemyip.provider_util as pru


class CheckIP(pro.AddressProvider):

    def fetch(self, options):
        return pru.fetch_url(
            "https://domains.google.com/checkip",
            timeout=options.timeout
        )
