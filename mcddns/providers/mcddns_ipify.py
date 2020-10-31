import mcddns.provider as provider


class IPv4(provider.AddressProvider):

    def fetch(self, options):
        return self.fetch_url(
            "https://api.ipify.org/",
            timeout=options.timeout
        )


class IPv6(provider.AddressProvider):

    def fetch(self, options):
        return self.fetch_url(
            "https://api6.ipify.org/",
            timeout=options.timeout
        )

    def validate(self, options, address):
        return self.is_ip_address(address)
