import abc
import importlib
import inspect
import ipaddress
import logging
import os
import pkgutil
import re
import requests
import sys
import mcddns.exceptions as exceptions
import mcddns.meta as meta


PROVIDER_MODULE_BUILTIN_PATH = os.path.join(
    os.path.dirname(__file__),
    "providers"
)
PROVIDER_MODULE_PREFIX = f"{meta.NAME}_"

log = logging.getLogger(__name__)


class Provider(abc.ABC):

    log = logging.getLogger(__name__)

    @classmethod
    def options_pre(cls, parser):
        pass

    @classmethod
    def options_post(cls, parser, options):
        pass


class AddressProvider(Provider):

    @classmethod
    @abc.abstractmethod
    def fetch(cls, options):
        pass

    @classmethod
    def validate(cls, options, address):
        return cls.is_ipv4_address(address)

    @staticmethod
    def fetch_url(url, timeout=3):
        try:
            return requests.get(url, timeout=timeout).text.strip()
        except requests.exceptions.RequestException as e:
            log.error(e)
            return None

    @staticmethod
    def is_ip_address(value):
        value = str(value)
        try:
            ipaddress.ip_address(value)
            log.debug("Valid IP address: %s", value)
            return True
        except ValueError:
            log.error("Invalid IP address: %s", value)
            return False

    @staticmethod
    def is_ipv4_address(value):
        value = str(value)
        try:
            if ipaddress.ip_address(value).version == 4:
                log.debug("Valid IPv4 address: %s", value)
                return True
            else:
                return False
        except ValueError:
            log.error("Invalid IPv4 address: %s", value)
            return False

    @staticmethod
    def is_ipv6_address(value):
        value = str(value)
        try:
            if ipaddress.ip_address(value).version == 6:
                log.debug("Valid IPv6 address: %s", value)
                return True
            else:
                return False
        except ValueError:
            log.error("Invalid IPv6 address: %s", value)
            return False

    @staticmethod
    def is_hostname(value):
        if len(value) > 255:
            result = False
        else:
            if value[-1] == ".":
                value = value[:-1]
            allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
            result = all(allowed.match(x) for x in value.split("."))

        if result:
            log.debug("Valid hostname: %s", value)
        else:
            log.error("Invalid hostname: %s", value)
        return result


class DNSProvider(Provider):

    @classmethod
    @abc.abstractmethod
    def check(cls, options, address):
        pass

    @classmethod
    @abc.abstractmethod
    def update(cls, options, address):
        pass


def import_modules(*paths):
    sys.path = list(paths) + sys.path
    modules = [
        m.name for m in pkgutil.iter_modules()
        if m.name.startswith(PROVIDER_MODULE_PREFIX)
    ]
    return {m: importlib.import_module(m) for m in modules}


def strip_prefix(value, prefix):
    return (
        value[len(prefix):]
        if prefix and value.startswith(prefix)
        else value
    )


def provider_full_name(obj):
    module_name = strip_prefix(
        inspect.getmodule(obj).__name__,
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
            raise exceptions.NoSuchProviderTypeError(
                f"Invalid provider types: {', '.join(invalid_types)}"
            )

    return {
        provider_full_name(cls): cls for cls
        in sum([t.__subclasses__() for t in types], [])
    }


def get_provider(name):
    try:
        return list_providers()[name]
    except KeyError:
        raise exceptions.NoSuchProviderError(f"No such provider: {name}")
