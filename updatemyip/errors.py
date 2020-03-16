class UpdateMyIpError(Exception):
    pass


class PluginError(UpdateMyIpError):
    pass


class NoSuchPluginError(PluginError):
    pass


class InvalidPluginTypeError(PluginError):
    pass


class InvalidPluginReturnTypeError(PluginError):
    pass


class DataValidationError(PluginError):
    pass
