import abc
import importlib as il
import inspect as ins
import logging as log
import os
import pkgutil as pu
import sys
import updatemyip.exceptions as exc
import updatemyip.meta as meta
import updatemyip.util as util
import updatemyip.validator as val

PROVIDER_MODULE_BUILTIN_PATH = os.path.join(
    os.path.dirname(__file__),
    "providers"
)
PROVIDER_MODULE_PREFIX = f"{meta.NAME}_"


class Provider(abc.ABC):

    def call(self, method, *args, **kwargs):
        obj_name = provider_full_name(self.__class__, PROVIDER_MODULE_PREFIX)
        log.debug(f"Calling provider method: {obj_name}.{method}()")
        return getattr(self, method)(*args, **kwargs)

    def options_pre(self, parser):
        pass

    def options_post(self, parser, options):
        pass


class AddressProvider(Provider):

    @abc.abstractmethod
    def fetch(self, options):
        pass

    def validate(self, options, address):
        return val.ipv4_address(address)


class DNSProvider(Provider):

    @abc.abstractmethod
    def check(self, options, address):
        pass

    @abc.abstractmethod
    def update(self, options, address):
        pass


def import_modules(*paths):
    sys.path = list(paths) + sys.path
    modules = [
        m.name for m in pu.iter_modules()
        if m.name.startswith(PROVIDER_MODULE_PREFIX)
    ]
    return {m: il.import_module(m) for m in modules}


def provider_full_name(obj, prefix=None):
    module = util.strip_prefix(ins.getmodule(obj).__name__, prefix)
    return f"{module}.{obj.__name__}"


def list_providers(*types):
    if not types:
        types = [AddressProvider, DNSProvider]

    return {
        f"{provider_full_name(cls, PROVIDER_MODULE_PREFIX)}": cls
        for cls in sum([type.__subclasses__() for type in types], [])
    }


def init_provider(name, *args, **kwargs):
    try:
        return list_providers()[name](*args, **kwargs)
    except KeyError:
        raise exc.NoSuchProviderError(f"No such provider: {name}")
