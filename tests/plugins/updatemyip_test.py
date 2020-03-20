import updatemyip.errors as err
import updatemyip.plugin as plugin


class Address(plugin.AddressPlugin):

    def fetch(self, options):
        return "127.0.0.1"


class AddressFalse(plugin.AddressPlugin):

    def fetch(self, options):
        return "Test"


class AddressError(plugin.AddressPlugin):

    def fetch(self, options):
        raise err.PluginError("Test")


class DNS(plugin.DNSPlugin):

    def options(self, parser):
        return "test dns options"

    def check(self, options, address):
        return True

    def update(self, options, address):
        return True


class DNSCheckFalse(plugin.DNSPlugin):

    def check(self, options, address):
        return False

    def update(self, options, address):
        return True


class DNSCheckError(plugin.DNSPlugin):

    def check(self, options, address):
        raise err.PluginError("Test")

    def update(self, options, address):
        return True


class DNSUpdateFalse(plugin.DNSPlugin):

    def check(self, options, address):
        return True

    def update(self, options, address):
        return False
