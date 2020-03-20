import logging as log
import time


def strip_prefix(value, prefix):
    return (
        value[len(prefix):]
        if prefix and value.startswith(prefix)
        else value
    )


def backoff(attempt, sleep=True):
    def fibonacci(n):
        if n == 0:
            return (0, 1)
        else:
            a, b = fibonacci(n // 2)
            c = a * (b * 2 - a)
            d = a * a + b * b
            return (c, d) if n % 2 == 0 else (d, c + d)

    delay = fibonacci(attempt)[1]
    if sleep and attempt:
        log.warning(f"Retrying in {delay}s...")
        time.sleep(delay)

    return delay
