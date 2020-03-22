import re
import updatemyip.provider as pro
import updatemyip.provider_util as pru


class CheckIP(pro.AddressProvider):

    def fetch(self, options):
        html = pru.fetch_url(
            "http://checkip.dyndns.com/",
            timeout=options.timeout
        )
        pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        matches = re.search(pattern, str(html), re.ASCII)
        return matches[0] if matches else None
