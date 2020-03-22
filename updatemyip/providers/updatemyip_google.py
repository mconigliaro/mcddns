import updatemyip.provider as pro


class CheckIP(pro.AddressProvider):

    def fetch(self, options):
        return self._fetch_url(options, "https://domains.google.com/checkip")
