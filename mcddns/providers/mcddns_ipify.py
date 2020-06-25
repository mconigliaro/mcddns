import mcddns.provider as provider


class IPv4(provider.AddressProvider):

    @classmethod
    def fetch(cls, options):
        return cls.fetch_url(
            "https://api.ipify.org/",
            timeout=options.timeout
        )


class IPv6(provider.AddressProvider):

    @classmethod
    def fetch(cls, options):
        return cls.fetch_url(
            "https://api6.ipify.org/",
            timeout=options.timeout
        )

    @classmethod
    def validate(cls, options, address):
        return cls.is_ip_address(address)
