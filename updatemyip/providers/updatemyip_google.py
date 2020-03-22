import requests as req
import updatemyip.exceptions as exc
import updatemyip.provider as pro


class CheckIP(pro.AddressProvider):

    def fetch(self, options):
        try:
            return req.get("https://domains.google.com/checkip",
                           timeout=options.timeout).text
        except req.exceptions.RequestException as e:
            raise exc.ProviderError(e) from e
