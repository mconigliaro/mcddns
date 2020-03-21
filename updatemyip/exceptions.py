class UpdateMyIpError(Exception):
    pass


class InvalidProviderTypeError(UpdateMyIpError):
    pass


class NoSuchProviderError(UpdateMyIpError):
    pass


class ProviderError(UpdateMyIpError):
    pass
