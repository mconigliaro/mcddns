import itertools as it
import logging as log
import updatemyip.exceptions as exc
import updatemyip.options as opt
import updatemyip.provider as pro
import updatemyip.util as util

RETURN_CODE_DRY_RUN = -2
RETURN_CODE_NOOP = -1
RETURN_CODE_SUCCESS = 0
RETURN_CODE_ERROR_ADDRESS = 1
RETURN_CODE_ERROR_DNS = 2


def main(default_address_providers=[], args=None):
    opts = opt.parse(default_address_providers, args)

    addr_providers = {p: pro.get_provider(p)() for p in opts.address_providers}
    providers = it.product(range(opts.retry + 1), addr_providers.items())
    for i, (provider_i, (provider_name, provider)) in enumerate(providers):
        util.backoff(i, max_retries=opts.retry, no_delay=opts.no_backoff)
        log.info(f"Using address provider: {provider_name}")
        try:
            address = provider.call("fetch", opts)
            log.info(f"Got address: {address}")
            if provider.call("validate", opts, address):
                break
        except exc.ProviderError as e:
            log.error(e)
        except Exception as e:
            log.exception(e)
    else:
        addr_provider_names = ', '.join(k for k in addr_providers.keys())
        log.critical(f"All address providers failed: {addr_provider_names}")
        return RETURN_CODE_ERROR_ADDRESS

    desired_record = f"{opts.fqdn} {opts.ttl} {opts.rrtype} {address}"
    provider = pro.get_provider(opts.dns_provider)()
    for i in range(opts.retry + 1):
        util.backoff(i, max_retries=opts.retry, no_delay=opts.no_backoff)
        log.info(f"Using DNS provider: {opts.dns_provider}")
        try:
            if provider.call("check", opts, address):
                if opts.dry_run:
                    log.info(f"DNS will be updated: {desired_record}")
                    return RETURN_CODE_DRY_RUN
                else:
                    if provider.call("update", opts, address):
                        log.info(f"DNS updated: {desired_record}")
                        return RETURN_CODE_SUCCESS
                    else:
                        log.error(f"DNS update failed")
            else:
                log.info(f"No DNS update required")
                return RETURN_CODE_NOOP
        except exc.ProviderError as e:
            log.error(e)
        except Exception as e:
            log.exception(e)
    else:
        log.critical(f"DNS provider failed: {opts.dns_provider}")
        return RETURN_CODE_ERROR_DNS
