import mcddns.provider as provider


class CheckIP(provider.AddressProvider):

    @classmethod
    def fetch(cls, options):
        return cls.fetch_url(
            "https://domains.google.com/checkip",
            timeout=options.timeout
        )
