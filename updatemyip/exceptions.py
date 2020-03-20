class UpdateMyIpError(Exception):
    pass


class NoSuchPluginError(UpdateMyIpError):
    pass


class PluginError(UpdateMyIpError):
    pass
