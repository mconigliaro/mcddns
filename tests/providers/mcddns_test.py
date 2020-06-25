import mcddns.provider as provider


class Address(provider.AddressProvider):

    @classmethod
    def fetch(cls, options):
        return "127.0.0.1"


class AddressFalse(provider.AddressProvider):

    @classmethod
    def fetch(cls, options):
        return "Test"


class AddressError(provider.AddressProvider):

    @classmethod
    def fetch(cls, options):
        raise Exception("Test")


class DNS(provider.DNSProvider):

    @classmethod
    def check(cls, options, address):
        return True

    @classmethod
    def update(cls, options, address):
        return True


class DNSCheckFalse(provider.DNSProvider):

    @classmethod
    def options_pre(cls, parser):
        parser.add_argument("--test", action="store_true", required=True)

    @classmethod
    def check(cls, options, address):
        return False

    @classmethod
    def update(cls, options, address):
        return True


class DNSCheckError(provider.DNSProvider):

    @classmethod
    def check(cls, options, address):
        raise Exception("Test")

    @classmethod
    def update(cls, options, address):
        return True


class DNSUpdateFalse(provider.DNSProvider):

    @classmethod
    def check(cls, options, address):
        return True

    @classmethod
    def update(cls, options, address):
        return False
