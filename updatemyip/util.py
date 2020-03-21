import logging as log
import time


def strip_prefix(value, prefix):
    return (
        value[len(prefix):]
        if prefix and value.startswith(prefix)
        else value
    )


def backoff(retry, max_retries=None, no_delay=False):
    def fibonacci(n):
        if n == 0:
            return (0, 1)
        else:
            a, b = fibonacci(n // 2)
            c = a * (b * 2 - a)
            d = a * a + b * b
            return (c, d) if n % 2 == 0 else (d, c + d)

    delay = fibonacci(retry)[1]

    if not no_delay and retry:
        if max_retries:
            counter = f"{retry}/{max_retries}"
            msg = f"[{counter}] Retrying in {delay}s..."
        else:
            msg = f"Retrying in {delay}s..."
        log.info(msg)
        time.sleep(delay)

    return delay
