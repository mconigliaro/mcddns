import importlib as il
import inspect as ins
import os
import pkgutil as pu
import sys
import updatemyip.errors as errors

PLUGIN_MODULE_PATHS = [
    os.path.join(
        os.getenv("XDG_CONFIG_HOME", os.path.join(os.getenv("HOME"), ".config")),
        __package__,
        "plugins",
    ),
    os.path.join(os.sep, "etc", __package__, "plugins"),
    os.path.join(os.path.dirname(__file__), "plugins"),
]
PLUGIN_MODULE_PREFIX = f"{__package__}_"

PLUGIN_TYPE_ADDRESS = 0
PLUGIN_TYPE_DNS = 1
PLUGIN_TYPES = (PLUGIN_TYPE_ADDRESS, PLUGIN_TYPE_DNS)

PLUGIN_STATUS_NOOP = 0
PLUGIN_STATUS_DRY_RUN = 1
PLUGIN_STATUS_SUCCESS = 2
PLUGIN_STATUS_FAILURE = 3

_PLUGIN_REGISTRY = {"plugin": {}, "options": {}}


def import_modules(*paths):
    sys.path = list(paths) + sys.path
    modules = [
        m.name for m in pu.iter_modules() if m.name.startswith(PLUGIN_MODULE_PREFIX)
    ]
    return {m: il.import_module(m) for m in modules}


def register_plugin(type):
    def wrapper(fn):
        if type not in PLUGIN_TYPES:
            raise errors.InvalidPluginTypeError(f"Invalid plugin type: {type}")
        full_name = _plugin_full_name(fn.__name__)
        _PLUGIN_REGISTRY["plugin"].setdefault(full_name, {})["type"] = type
        _PLUGIN_REGISTRY["plugin"][full_name]["plugin_fn"] = fn

    return wrapper


def register_options(plugin):
    def wrapper(fn):
        full_name = _plugin_full_name(plugin)
        _PLUGIN_REGISTRY["options"][full_name] = fn

    return wrapper


def list_plugins(type):
    if type not in PLUGIN_TYPES:
        raise errors.InvalidPluginTypeError(f"Invalid plugin type: {type}")
    return [
        name
        for name, info in _PLUGIN_REGISTRY["plugin"].items()
        if info["type"] == type
    ]


def get_plugin(name):
    try:
        return _PLUGIN_REGISTRY["plugin"][name]["plugin_fn"]
    except KeyError as e:
        raise errors.NoSuchPluginError(f"No such plugin: {name}")


def add_options(parser):
    return [
        fn(parser=parser.add_argument_group(f"{name} arguments"))
        for name, fn in _PLUGIN_REGISTRY["options"].items()
        if name in _PLUGIN_REGISTRY["plugin"].keys()
    ]


def _plugin_full_name(plugin):
    caller = ins.getmodule(ins.stack()[2][0]).__name__
    module = _strip_module_prefix(caller)
    return f"{module}.{plugin}"


def _strip_module_prefix(name):
    return name[len(PLUGIN_MODULE_PREFIX) :]
