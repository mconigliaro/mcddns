import updatemyip.provider as pro


class Address(pro.AddressProvider):

    def fetch(self, options):
        return "127.0.0.1"


class AddressFalse(pro.AddressProvider):

    def fetch(self, options):
        return "Test"


class AddressError(pro.AddressProvider):

    def fetch(self, options):
        raise Exception("Test")


class DNS(pro.DNSProvider):

    def check(self, options, address):
        return True

    def update(self, options, address):
        return True


class DNSCheckFalse(pro.DNSProvider):

    def options_pre(self, parser):
        parser.add_argument("--test", action="store_true", required=True)

    def check(self, options, address):
        return False

    def update(self, options, address):
        return True


class DNSCheckError(pro.DNSProvider):

    def check(self, options, address):
        raise Exception("Test")

    def update(self, options, address):
        return True


class DNSUpdateFalse(pro.DNSProvider):

    def check(self, options, address):
        return True

    def update(self, options, address):
        return False
