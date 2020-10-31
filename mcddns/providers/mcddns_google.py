import mcddns.provider as provider


class CheckIP(provider.AddressProvider):

    def fetch(self, options):
        return self.fetch_url(
            "https://domains.google.com/checkip",
            timeout=options.timeout
        )
