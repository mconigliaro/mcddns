import itertools
import logging
import os
import tempfile
import time
import mcddns.meta as meta
import mcddns.provider as provider

RETURN_CODE_DRY_RUN = 100
RETURN_CODE_DNS_NOOP = 101
RETURN_CODE_DNS_UPDATED = 201
RETURN_CODE_ADDRESS_ERROR = 300
RETURN_CODE_DNS_ERROR = 301

RETURN_CODES_SUCCESS = range(100, 300)

CRON_IGNORE_RETURN_CODE_CLASS_TRANSITIONS = (
    (None, 1),
    (1, 1),
    (2, 1),
    (3, 3)
)

EXIT_CODE_SUCCESS = 0
EXIT_CODE_ERROR = 1

STATE_PATH = os.path.join(tempfile.gettempdir(), f"{meta.NAME}.state")


log = logging.getLogger(__name__)


def main(opts):
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
        return RETURN_CODE_ADDRESS_ERROR

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
                        return RETURN_CODE_DNS_UPDATED
                    else:
                        log.error("DNS update failed")
            else:
                log.info("No DNS update required")
                return RETURN_CODE_DNS_NOOP
        except Exception as e:
            log.exception(e)
    else:
        log.critical("DNS provider failed: %s", opts.dns_provider)
        return RETURN_CODE_DNS_ERROR


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


def state_exists(path=STATE_PATH):
    exists = os.path.isfile(path)
    if exists:
        log.debug("Found previous state: %s", path)
    else:
        log.debug("No previous state found: %s", path)
    return exists


def state_read(path=STATE_PATH):
    if state_exists(path):
        try:
            with open(path, 'r') as f:
                data = f.read()
                log.debug("Read state: %s", data)
            return data
        except OSError as e:
            log.error("Unable to read state: %s", e)
            return ""
    else:
        return ""


def state_write(data, path=STATE_PATH):
    try:
        with open(path, 'w') as f:
            log.debug("Writing state: %s", data)
            f.write(str(data))
        return True
    except OSError as e:
        log.error("Unable to write state: %s", e)
        return False


def state_remove(path=STATE_PATH):
    if state_exists(path):
        try:
            log.debug("Removing previous state: %s", path)
            os.remove(path)
        except OSError as e:
            log.error("Unable to remove state: %s", e)
            return False
    return True


def return_code_class(return_code):
    try:
        return int(str(return_code)[0])
    except IndexError:
        None


def return_code_class_transition(return_code1, return_code2):
    return (
        return_code_class(return_code1),
        return_code_class(return_code2)
    )


def exit_code(return_code, cron=False, state_path=STATE_PATH):
    if return_code in RETURN_CODES_SUCCESS:
        exit_code = EXIT_CODE_SUCCESS
    else:
        exit_code = EXIT_CODE_ERROR

    if cron:
        previous_return_code = state_read(state_path)
        if str(return_code) != previous_return_code:
            state_write(return_code, path=state_path)

        transition = return_code_class_transition(
            previous_return_code,
            return_code
        )
        if transition in CRON_IGNORE_RETURN_CODE_CLASS_TRANSITIONS:
            cron_exit_code = EXIT_CODE_SUCCESS
        else:
            cron_exit_code = EXIT_CODE_ERROR

        if cron_exit_code == exit_code:
            log.debug("Exit code: %d", exit_code)
        else:
            log.debug(
                "Rewriting exit code for cron: %d => %d",
                exit_code, cron_exit_code
            )
            exit_code = cron_exit_code

    return exit_code
