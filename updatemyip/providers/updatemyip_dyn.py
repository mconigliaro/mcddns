import re
import requests as req
import updatemyip.exceptions as exc
import updatemyip.provider as pro


class CheckIP(pro.AddressProvider):

    def fetch(self, options):
        try:
            html = req.get("http://checkip.dyndns.com/",
                           timeout=options.timeout).text
            pattern = r"\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}"
            return re.search(pattern, html, re.ASCII)[0]
        except req.exceptions.RequestException as e:
            raise exc.ProviderError(e) from e
