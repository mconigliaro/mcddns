import updatemyip.exceptions as exc
import updatemyip.provider as pro


class Address(pro.AddressProvider):

    def fetch(self, options):
        return "127.0.0.1"


class AddressFalse(pro.AddressProvider):

    def fetch(self, options):
        return "Test"


class AddressError(pro.AddressProvider):

    def fetch(self, options):
        raise exc.ProviderError("Test")


class DNS(pro.DNSProvider):

    def options(self, parser):
        return "test dns options"

    def check(self, options, address):
        return True

    def update(self, options, address):
        return True


class DNSCheckFalse(pro.DNSProvider):

    def check(self, options, address):
        return False

    def update(self, options, address):
        return True


class DNSCheckError(pro.DNSProvider):

    def check(self, options, address):
        raise exc.ProviderError("Test")

    def update(self, options, address):
        return True


class DNSUpdateFalse(pro.DNSProvider):

    def check(self, options, address):
        return True

    def update(self, options, address):
        return False
