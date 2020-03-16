import importlib as il
import inspect as ins
import ipaddress as ip
import os
import pkgutil as pu
import socket as so
import sys
import updatemyip.meta as meta
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
PLUGIN_MODULE_PREFIX = f"{meta.NAME}_"

PLUGIN_TYPE_ADDRESS = 0
PLUGIN_TYPE_DNS = 1
PLUGIN_TYPES = (PLUGIN_TYPE_ADDRESS, PLUGIN_TYPE_DNS)

PLUGIN_RETURN_TYPE_IP_ADDRESS = 0
PLUGIN_RETURN_TYPE_IP_ADDRESS_PRIVATE = 1
PLUGIN_RETURN_TYPE_IP_ADDRESS_GLOBAL = 2
PLUGIN_RETURN_TYPE_HOSTNAME = 3
PLUGIN_RETURN_TYPES = (
    PLUGIN_RETURN_TYPE_IP_ADDRESS,
    PLUGIN_RETURN_TYPE_IP_ADDRESS_PRIVATE,
    PLUGIN_RETURN_TYPE_IP_ADDRESS_GLOBAL,
    PLUGIN_RETURN_TYPE_HOSTNAME,
)

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


def plugin_full_name(plugin):
    caller = ins.getmodule(ins.stack()[2][0]).__name__
    module = strip_module_prefix(caller)
    return f"{module}.{plugin}"


def strip_module_prefix(name):
    return (
        name[len(PLUGIN_MODULE_PREFIX) :]
        if name.startswith(PLUGIN_MODULE_PREFIX)
        else name
    )


def register_address_plugin(return_type):
    def wrapper(function):
        if return_type not in PLUGIN_RETURN_TYPES:
            raise errors.InvalidPluginReturnTypeError(
                f"Invalid plugin return type: {return_type}"
            )
        full_name = plugin_full_name(function.__name__)
        _PLUGIN_REGISTRY["plugin"][full_name] = {
            "plugin_type": PLUGIN_TYPE_ADDRESS,
            "return_type": return_type,
            "function": function,
        }

    return wrapper


def register_dns_plugin():
    def wrapper(function):
        full_name = plugin_full_name(function.__name__)
        _PLUGIN_REGISTRY["plugin"][full_name] = {
            "plugin_type": PLUGIN_TYPE_DNS,
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
        if info["plugin_type"] == type
    ]


def get_plugin(name):
    try:
        return _PLUGIN_REGISTRY["plugin"][name]
    except KeyError as e:
        raise errors.NoSuchPluginError(f"No such plugin: {name}")


def call_address_plugin_function(name, *args, **kwargs):
    p = get_plugin(name)
    result = p["function"](*args, **kwargs)
    {
        PLUGIN_RETURN_TYPE_IP_ADDRESS: to_ip_address,
        PLUGIN_RETURN_TYPE_IP_ADDRESS_PRIVATE: is_ip_address_private,
        PLUGIN_RETURN_TYPE_IP_ADDRESS_GLOBAL: is_ip_address_global,
        PLUGIN_RETURN_TYPE_HOSTNAME: is_hostname,
    }[p["return_type"]](result)

    return result


def call_dns_plugin_function(name, *args, **kwargs):
    return get_plugin(name)["function"](*args, **kwargs)


def to_ip_address(value):
    try:
        return ip.ip_address(value)
    except ValueError:
        raise errors.DataValidationError(f"Expected IP address but got: {value}")


def is_ip_address_private(value):
    if to_ip_address(value).is_private:
        return True
    else:
        raise errors.DataValidationError(
            f"Expected private IP address but got: {value}"
        )


def is_ip_address_global(value):
    if to_ip_address(value).is_global:
        return True
    else:
        raise errors.DataValidationError(f"Expected global IP address but got: {value}")


# FIXME: Needs better validation
def is_hostname(value):
    try:
        so.gethostbyname(value)
        return True
    except so.error:
        raise errors.DataValidationError(f"Expected hostname but got: {value}")


def list_plugin_options():
    return {
        name: fn
        for name, fn in _PLUGIN_REGISTRY["options"].items()
        if name in _PLUGIN_REGISTRY["plugin"]
    }
