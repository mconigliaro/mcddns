import re
import updatemyip.provider as pro


class CheckIP(pro.AddressProvider):

    def fetch(self, options):
        html = self._fetch_url(options, "http://checkip.dyndns.com/")
        pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
        return re.search(pattern, html, re.ASCII)[0]
