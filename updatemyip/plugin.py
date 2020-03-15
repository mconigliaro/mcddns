import importlib as il
import inspect as ins
import os
import pkgutil as pu
import sys
import updatemyip.errors as errors

MODULE_PREFIX = f"{__package__}_"

PLUGIN_TYPE_ADDRESS = 0
PLUGIN_TYPE_DNS = 1
PLUGIN_TYPES = (PLUGIN_TYPE_ADDRESS, PLUGIN_TYPE_DNS)

_PLUGIN_REGISTRY = {}
_PLUGIN_OPTIONS = {}

PLUGIN_STATUS_NOOP = 0
PLUGIN_STATUS_SUCCESS = 1
PLUGIN_STATUS_FAILURE = 2


def import_modules():
    sys.path.append(os.path.join(os.path.dirname(__file__), "plugins"))
    modules = [m.name for m in pu.iter_modules() if m.name.startswith(MODULE_PREFIX)]
    return {m: il.import_module(m) for m in modules}


def register_plugin(type):
    def wrapper(fn):
        if type not in PLUGIN_TYPES:
            raise errors.InvalidPluginTypeError(f"Invalid plugin type: {type}")
        full_name = _plugin_full_name(fn.__name__)
        _PLUGIN_REGISTRY.setdefault(full_name, {})["type"] = type
        _PLUGIN_REGISTRY[full_name]["plugin_fn"] = fn

    return wrapper


def register_options(plugin):
    def wrapper(fn):
        full_name = _plugin_full_name(plugin)
        _PLUGIN_OPTIONS[full_name] = fn

    return wrapper


def list_plugins(type):
    if type not in PLUGIN_TYPES:
        raise errors.InvalidPluginTypeError(f"Invalid plugin type: {type}")
    return [name for name, info in _PLUGIN_REGISTRY.items() if info["type"] == type]


def get_plugin(name):
    try:
        return _PLUGIN_REGISTRY[name]["plugin_fn"]
    except KeyError as e:
        raise errors.NoSuchPluginError(f"No such plugin: {name}")


def add_arguments(parser):
    for name, fn in _PLUGIN_OPTIONS.items():
        if name not in _PLUGIN_REGISTRY.keys():
            raise errors.NoSuchPluginError(f"No such plugin: {name}")
        else:
            fn(parser.add_argument_group(f"{name} arguments"))


def _plugin_full_name(fn):
    module = ins.getmodule(ins.stack()[2][0]).__name__[len(MODULE_PREFIX) :]
    return f"{module}.{fn}"
