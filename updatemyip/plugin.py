import importlib as il
import inspect as ins
import os
import pkgutil as pu
import sys

MODULE_PREFIX = f"{__package__}_"

PLUGIN_TYPE_ADDRESS = 0
PLUGIN_TYPE_DNS = 1
PLUGIN_TYPES = (PLUGIN_TYPE_ADDRESS, PLUGIN_TYPE_DNS)

_PLUGIN_REGISTRY = {}

PLUGIN_STATUS_NOOP = 0
PLUGIN_STATUS_SUCCESS = 1
PLUGIN_STATUS_FAILURE = 2


class PluginError(Exception):
    pass


class UnknownPluginError(PluginError):
    pass


class InvalidPluginTypeError(PluginError):
    pass


def import_modules():
    sys.path.append(os.path.join(os.path.dirname(__file__), "plugins"))
    modules = [m.name for m in pu.iter_modules() if m.name.startswith(MODULE_PREFIX)]
    return {m: il.import_module(m) for m in modules}


def register_plugin(type):
    def wrapper(fn):
        if type not in PLUGIN_TYPES:
            raise InvalidPluginTypeError(f"Invalid plugin type: {type}")
        module = ins.getmodule(ins.stack()[1][0]).__name__[len(MODULE_PREFIX) :]
        _PLUGIN_REGISTRY[f"{module}.{fn.__name__}"] = {"type": type, "function": fn}

    return wrapper


def list_plugins(type):
    if type not in PLUGIN_TYPES:
        raise InvalidPluginTypeError(f"Invalid plugin type: {type}")
    return [name for name, info in _PLUGIN_REGISTRY.items() if info["type"] == type]


def get_plugin(name):
    try:
        return _PLUGIN_REGISTRY[name]
    except KeyError as e:
        raise UnknownPluginError(f"Unknown plugin: {name}")
