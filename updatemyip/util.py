import inspect as ins
import logging as log
import time


def strip_prefix(value, prefix):
    return (
        value[len(prefix):]
        if prefix and value.startswith(prefix)
        else value
    )


def plugin_full_name(cls, prefix=None):
    module = strip_prefix(ins.getmodule(cls).__name__, prefix)
    return f"{module}.{cls.__name__}"  # FIXME: Make snake case?


def fibonacci_backoff(attempt, sleep=True):
    def fibonacci(n):
        if n == 0:
            return (0, 1)
        else:
            a, b = fibonacci(n // 2)
            c = a * (b * 2 - a)
            d = a * a + b * b
            return (c, d) if n % 2 == 0 else (d, c + d)

    fib = fibonacci(attempt)[1]
    if attempt and sleep:
        sleep = fib
        log.info(f"Retrying in {sleep}s...")
        time.sleep(sleep)

    return fib
