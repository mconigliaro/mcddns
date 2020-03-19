import abc
import importlib as il
import os
import pkgutil as pu
import sys
import updatemyip.errors as err
import updatemyip.meta as meta
import updatemyip.util as util
import updatemyip.validator as val

PLUGIN_MODULE_BUILTIN_PATH = os.path.join(os.path.dirname(__file__), "plugins")
PLUGIN_MODULE_PREFIX = f"{meta.NAME}_"

PLUGIN_STATUS_NOOP = 0
PLUGIN_STATUS_DRY_RUN = 1
PLUGIN_STATUS_SUCCESS = 2
PLUGIN_STATUS_FAILURE = 3


class Plugin(abc.ABC):

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
    [sys.path.insert(0, path) for path in paths if path not in sys.path]
    modules = [
        m.name for m in pu.iter_modules()
        if m.name.startswith(PLUGIN_MODULE_PREFIX)
    ]
    return {m: il.import_module(m) for m in modules}


def list_plugins(*types):
    if not types:
        types = [AddressPlugin, DNSPlugin]

    return {
        f"{util.plugin_full_name(c, PLUGIN_MODULE_PREFIX)}": c
        for c in sum([type.__subclasses__() for type in types], [])
    }


def get_plugin(name):
    try:
        return list_plugins()[name]
    except KeyError:
        raise err.NoSuchPluginError(f"No such plugin: {name}")
