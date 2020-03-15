import argparse as ap

parser = ap.ArgumentParser()


class Options(ap.Namespace):
    pass


def log(options):
    # FIXME: Sort options
    return ", ".join(f"{k}={repr(v)}" for k, v in vars(options).items())
