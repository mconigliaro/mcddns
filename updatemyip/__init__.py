import itertools
import logging
import time
import updatemyip.options as options
import updatemyip.provider as provider

RETURN_CODE_DRY_RUN = -2
RETURN_CODE_NOOP = -1
RETURN_CODE_SUCCESS = 0
RETURN_CODE_ERROR_ADDRESS = 1
RETURN_CODE_ERROR_DNS = 2

log = logging.getLogger(__name__)


def main(default_address_providers=[], args=None):
    opts = options.parse(default_address_providers, args)
    tries = opts.retry + 1

    addr_providers = {p: provider.get_provider(p)
                      for p in opts.address_providers}
    addr_providers_with_retry = iterate_with_retry(
         addr_providers.items(),
         tries=tries,
         no_backoff=opts.no_backoff
    )
    for provider_name, provider_cls in addr_providers_with_retry:
        log.info("Using address provider: %s", provider_name)
        try:
            address = provider_cls.fetch(opts)
            log.info("Got address: %s", address)
            if provider_cls.validate(opts, address):
                break
        except Exception as e:
            log.exception(e)
    else:
        addr_provider_names = ', '.join(addr_providers.keys())
        log.critical("All address providers failed: %s", addr_provider_names)
        return RETURN_CODE_ERROR_ADDRESS

    desired_record = f"{opts.fqdn} {opts.ttl} {opts.rrtype} {address}"

    dns_providers_with_retry = iterate_with_retry(
        [provider.get_provider(opts.dns_provider)],
        tries=tries,
        no_backoff=opts.no_backoff
    )
    for provider_cls in dns_providers_with_retry:
        log.info("Using DNS provider: %s", opts.dns_provider)
        try:
            if provider_cls.check(opts, address):
                if opts.dry_run:
                    log.info("DNS will be updated: %s", desired_record)
                    return RETURN_CODE_DRY_RUN
                else:
                    if provider_cls.update(opts, address):
                        log.info("DNS updated: %s", desired_record)
                        return RETURN_CODE_SUCCESS
                    else:
                        log.error("DNS update failed")
            else:
                log.info("No DNS update required")
                return RETURN_CODE_NOOP
        except Exception as e:
            log.exception(e)
    else:
        log.critical("DNS provider failed: %s", opts.dns_provider)
        return RETURN_CODE_ERROR_DNS


def fibonacci(n):
    if n == 0:
        return 0, 1
    else:
        a, b = fibonacci(n // 2)
        c = a * (b * 2 - a)
        d = a * a + b * b
        return (c, d) if n % 2 == 0 else (d, c + d)


def iterate_with_retry(iterable, tries=3, no_backoff=False):
    chain = list(itertools.chain.from_iterable(
        itertools.repeat(iterable, tries))
    )
    retries = len(chain) - 1
    for i, obj in enumerate(chain):
        if i:
            if no_backoff:
                log.info("Retrying (%d/%d)", i, retries)
            else:
                delay = fibonacci(i)[1]
                log.info("Retrying (%d/%d) in %ds...", i, retries, delay)
                time.sleep(delay)

        yield obj
