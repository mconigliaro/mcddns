class UpdateMyIpError(Exception):
    pass


class PluginError(UpdateMyIpError):
    pass


class NoSuchPluginError(PluginError):
    pass


class InvalidPluginTypeError(PluginError):
    pass


class ValidationError(PluginError):
    pass
