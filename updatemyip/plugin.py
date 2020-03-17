import importlib as il
import inspect as ins
import logging as log
import os
import pkgutil as pu
import sys
import updatemyip.meta as meta
import updatemyip.errors as errors

PLUGIN_MODULE_BUILTIN_PATH = os.path.join(os.path.dirname(__file__), "plugins")
PLUGIN_MODULE_PREFIX = f"{meta.NAME}_"

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
        m.name for m in pu.iter_modules()
        if m.name.startswith(PLUGIN_MODULE_PREFIX)
    ]
    return {m: il.import_module(m) for m in modules}


def plugin_full_name(plugin):
    caller = ins.getmodule(ins.stack()[2][0]).__name__
    module = strip_module_prefix(caller)
    return f"{module}.{plugin}"


def strip_module_prefix(name):
    return (
        name[len(PLUGIN_MODULE_PREFIX):]
        if name.startswith(PLUGIN_MODULE_PREFIX)
        else name
    )


def register_address_plugin(validator):
    def wrapper(function):
        full_name = plugin_full_name(function.__name__)
        _PLUGIN_REGISTRY["plugin"][full_name] = {
            "type": PLUGIN_TYPE_ADDRESS,
            "validator": validator,
            "function": function,
        }

    return wrapper


def register_dns_plugin():
    def wrapper(function):
        full_name = plugin_full_name(function.__name__)
        _PLUGIN_REGISTRY["plugin"][full_name] = {
            "type": PLUGIN_TYPE_DNS,
            "function": function,
        }

    return wrapper


def register_plugin_options(plugin):
    def wrapper(function):
        full_name = plugin_full_name(plugin)
        _PLUGIN_REGISTRY["options"][full_name] = function

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
        return _PLUGIN_REGISTRY["plugin"][name]
    except KeyError:
        raise errors.NoSuchPluginError(f"No such plugin: {name}")


def call_address_plugin(name, *args, **kwargs):
    p = get_plugin(name)
    address = p["function"](*args, **kwargs)
    log.info(f"Got address: {address}")

    validator_fn = p["validator"]
    if callable(validator_fn):
        validator_log = f"{validator_fn.__name__}('{address})"
        log.debug(f"Calling validator: {validator_log}")
        if not validator_fn(address):
            raise errors.ValidationError(
                f"Validator failed: {validator_log}")

    return address


def call_dns_plugin(name, *args, **kwargs):
    return get_plugin(name)["function"](*args, **kwargs)


def list_plugin_options():
    return {
        name: fn
        for name, fn in _PLUGIN_REGISTRY["options"].items()
        if name in _PLUGIN_REGISTRY["plugin"]
    }
