import requests as req
import updatemyip.options as options


options.parser.add_argument("--ipify-ip-version", type=int, choices=(4, 6), default=4)


def get_addr(options):
    if options["ipify_ip_version"] == 4:
        return req.get("https://api.ipify.org").text
    elif options["ipify_ip_version"] == 6:
        return req.get("https://api6.ipify.org").text
