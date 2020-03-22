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
import updatemyip.provider_util as pru

PROVIDER_MODULE_BUILTIN_PATH = os.path.join(
    os.path.dirname(__file__),
    "providers"
)
PROVIDER_MODULE_PREFIX = f"{meta.NAME}_"


class Provider(abc.ABC):

    def call(self, method, *args, **kwargs):
        obj_name = provider_full_name(self.__class__)
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
        return pru.is_ipv4_address(address)


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


def provider_full_name(obj):
    module_name = util.strip_prefix(
        ins.getmodule(obj).__name__,
        PROVIDER_MODULE_PREFIX
    )
    return f"{module_name}.{obj.__name__}"


def list_providers(*types):
    valid_types = Provider.__subclasses__()

    if not [t for t in types if t]:
        types = valid_types
    else:
        invalid_types = [str(t) for t in types if t not in valid_types]
        if invalid_types:
            raise exc.NoSuchProviderTypeError(
                f"Invalid provider types: {', '.join(invalid_types)}"
            )

    return {
        f"{provider_full_name(cls)}": cls
        for cls in sum([t.__subclasses__() for t in types], [])
    }


def get_provider(name):
    try:
        return list_providers()[name]
    except KeyError:
        raise exc.NoSuchProviderError(f"No such provider: {name}")
