class MCDDNSError(Exception):
    pass


class NoSuchProviderTypeError(MCDDNSError):
    pass


class NoSuchProviderError(MCDDNSError):
    pass
