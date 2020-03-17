import ipaddress as ip
import re


def ip_address(value):
    try:
        ip.ip_address(value)
        return True
    except ValueError:
        return False


def ipv4_address(value):
    try:
        return ip.ip_address(value).version == 4
    except ValueError:
        return False


def ipv6_address(value):
    try:
        return ip.ip_address(value).version == 6
    except ValueError:
        return False


# https://stackoverflow.com/a/2532344
def hostname(value):
    if len(value) > 255:
        return False
    if value[-1] == ".":
        value = value[:-1]
    allowed = re.compile(r"(?!-)[A-Z\d-]{1,63}(?<!-)$", re.IGNORECASE)
    return all(allowed.match(x) for x in value.split("."))
