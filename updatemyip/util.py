import logging as log
import time


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
