import ipaddress as ip
import logging as log
import re
import requests as req
import updatemyip.exceptions as exc


def fetch_url(url, timeout=15):
    try:
        return req.get(url, timeout=timeout).text.strip()
    except req.exceptions.RequestException as e:
        raise exc.ProviderError(e) from e


def is_ip_address(value):
    try:
        ip.ip_address(value)
        log.debug(f"Valid IP address: {value}")
        return True
    except ValueError:
        log.error(f"Invalid IP address: {value}")
        return False


def is_ipv4_address(value):
    try:
        if ip.ip_address(value).version == 4:
            log.debug(f"Valid IPv4 address: {value}")
            return True
        else:
            return False
    except ValueError:
        log.error(f"Invalid IPv4 address: {value}")
        return False


def is_ipv6_address(value):
    try:
        if ip.ip_address(value).version == 6:
            log.debug(f"Valid IPv6 address: {value}")
            return True
        else:
            return False
    except ValueError:
        log.error(f"Invalid IPv6 address: {value}")
        return False


def is_hostname(value):
    if len(value) > 255:
        result = False
    else:
        if value[-1] == ".":
            value = value[:-1]
        allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
        result = all(allowed.match(x) for x in value.split("."))

    if result:
        log.debug(f"Valid hostname: {value}")
    else:
        log.error(f"Invalid hostname: {value}")
    return result
