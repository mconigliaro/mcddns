class UpdateMyIpError(Exception):
    pass


class NoSuchProviderError(UpdateMyIpError):
    pass


class ProviderError(UpdateMyIpError):
    pass
