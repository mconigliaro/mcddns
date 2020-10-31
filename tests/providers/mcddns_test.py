import mcddns.provider as provider


class Address(provider.AddressProvider):

    def fetch(self, options):
        return "127.0.0.1"


class AddressFalse(provider.AddressProvider):

    def fetch(self, options):
        return "Test"


class AddressError(provider.AddressProvider):

    def fetch(self, options):
        raise Exception("Test")


class DNS(provider.DNSProvider):

    def check(self, options, address):
        return True

    def update(self, options, address):
        return True


class DNSCheckFalse(provider.DNSProvider):

    def options_pre(self, parser):
        parser.add_argument("--test", action="store_true", required=True)

    def check(self, options, address):
        return False

    def update(self, options, address):
        return True


class DNSCheckError(provider.DNSProvider):

    def check(self, options, address):
        raise Exception("Test")

    def update(self, options, address):
        return True


class DNSUpdateFalse(provider.DNSProvider):

    def check(self, options, address):
        return True

    def update(self, options, address):
        return False
