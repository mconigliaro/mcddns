class UpdateMyIPError(Exception):
    pass


class NoSuchProviderTypeError(UpdateMyIPError):
    pass


class NoSuchProviderError(UpdateMyIPError):
    pass
