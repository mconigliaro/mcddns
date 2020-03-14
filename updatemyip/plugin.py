import importlib as il
import pkgutil as pu


PLUGIN_PREFIX = "updatemyip_"
PLUGIN_ADDR_FN = "get_addr"
PLUGIN_DNS_FN = "update_dns"

PLUGIN_NOOP = 0
PLUGIN_SUCCESS = 1
PLUGIN_FAILURE = 2


def list_plugins(prefix=PLUGIN_PREFIX):
    return [p.name for p in pu.iter_modules() if p.name.startswith(prefix)]


def import_plugins(
    plugins, prefix=PLUGIN_PREFIX, addr_fn=PLUGIN_ADDR_FN, dns_fn=PLUGIN_DNS_FN
):
    addr_plugins = {}
    dns_plugins = {}
    for p in plugins:
        module = il.import_module(p)
        plugin_name = p[len(prefix) :]
        dir_module = dir(module)
        if addr_fn in dir_module:
            addr_plugins[plugin_name] = module
        if dns_fn in dir_module:
            dns_plugins[plugin_name] = module
    return addr_plugins, dns_plugins
