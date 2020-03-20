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

PLUGIN_MODULE_BUILTIN_PATH = os.path.join(os.path.dirname(__file__), "plugins")
PLUGIN_MODULE_PREFIX = f"{meta.NAME}_"


class Plugin(abc.ABC):

    def call(self, method, *args, **kwargs):
        obj_name = plugin_full_name(self.__class__, PLUGIN_MODULE_PREFIX)
        log.debug(f"Calling plugin method: {obj_name}.{method}()")
        return getattr(self, method)(*args, **kwargs)

    def options(self, parser):
        pass


class AddressPlugin(Plugin):

    @abc.abstractmethod
    def fetch(self, options):
        pass

    def validate(self, options, address):
        return val.ipv4_address(address)


class DNSPlugin(Plugin):

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
        if m.name.startswith(PLUGIN_MODULE_PREFIX)
    ]
    return {m: il.import_module(m) for m in modules}


def plugin_full_name(obj, prefix=None):
    module = util.strip_prefix(ins.getmodule(obj).__name__, prefix)
    return f"{module}.{obj.__name__}"


def list_plugins(*types):
    if not types:
        types = [AddressPlugin, DNSPlugin]

    return {
        f"{plugin_full_name(cls, PLUGIN_MODULE_PREFIX)}": cls
        for cls in sum([type.__subclasses__() for type in types], [])
    }


def init_plugin(name, *args, **kwargs):
    try:
        return list_plugins()[name](*args, **kwargs)
    except KeyError:
        raise exc.NoSuchPluginError(f"No such plugin: {name}")
