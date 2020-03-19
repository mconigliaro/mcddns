import updatemyip.plugin as plugin
import updatemyip.validator as validator


class Address(plugin.AddressPlugin):

    def fetch(self, options):
        return "127.0.0.1"

    def validate(self, options, address):
        return validator.ipv4_address(address)


class AddressFail(plugin.AddressPlugin):

    def fetch(self, options):
        return "fail"

    def validate(self, options, address):
        return validator.ipv4_address(address)


class DNS(plugin.DNSPlugin):

    def options(self, parser):
        return "test dns options"

    def check(self, options, address):
        return True

    def update(self, options, address):
        return plugin.PLUGIN_STATUS_SUCCESS


class DNSNoOp(plugin.DNSPlugin):

    def check(self, options, address):
        return False

    def update(self, options, address):
        return plugin.PLUGIN_STATUS_NOOP


class DNSDryRun(plugin.DNSPlugin):

    def check(self, options, address):
        return True

    def update(self, options, address):
        return plugin.PLUGIN_STATUS_DRY_RUN


class DNSFail(plugin.DNSPlugin):

    def check(self, options, address):
        return True

    def update(self, options, address):
        return plugin.PLUGIN_STATUS_FAILURE
