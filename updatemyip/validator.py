import ipaddress as ip
import re
import socket as so


def is_ip_address(value):
    try:
        ip.ip_address(value)
        return True
    except ValueError:
        return False


def is_ip_address_private(value):
    try:
        return ip.ip_address(value).is_private
    except ValueError:
        return False


def is_ip_address_global(value):
    try:
        return ip.ip_address(value).is_global
    except ValueError:
        return False


# https://stackoverflow.com/a/2532344
def is_hostname(value):
    if len(value) > 255:
        return False
    if value[-1] == ".":
        value = value[:-1]
    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in value.split("."))


def is_hostname_private(value):
    if is_hostname(value):
        try:
            return is_ip_address_private(so.gethostbyname(value))
        except so.error:
            return False
    else:
        return False


def is_hostname_global(value):
    if is_hostname(value):
        try:
            return is_ip_address_global(so.gethostbyname(value))
        except so.error:
            return False
    else:
        return False
