class UpdateMyIpError(Exception):
    pass


class NoSuchProviderTypeError(UpdateMyIpError):
    pass


class NoSuchProviderError(UpdateMyIpError):
    pass
