# Update My IP

Industrial-strength dynamic DNS client

## Features

- Extensible plugin-oriented architecture
- Built-in address provider result validation
- Address provider redundancy with optional retry and Fibonacci backoff
- Detailed logging
- Dry-run mode

### Built-In Providers

#### Address

Address providers are responsible for obtaining an address.

- `aws.CheckIP`: URL provided by [Amazon Web Services](https://aws.amazon.com/)
- `dyn.CheckIP`: URL provided by [Dyn](https://dyn.com/)
- `google.CheckIP`: URL provided by [Google Domains](https://domains.google.com)
- `ipify.IPv4`: URL provided by [ipify](https://www.ipify.org/)
- `ipify.IPv6`: URL provided by [ipify](https://www.ipify.org/) (IPv6)

#### DNS

DNS providers are responsible for managing a DNS record.

- `aws.Route53`: Uses [Amazon Route53](https://aws.amazon.com/route53/)

## Installation

    pip install updatemyip

## Running the Application

    updatemyip <dns_provider> <fqdn> [options]

Use `--help` to see available options.

## Development

### Getting Started

    pip install pipenv
    pipenv install --dev
    pipenv shell
    ...

### Running Tests

    pytest

### Writing Providers

In production mode, Python modules/packages prefixed with `updatemyip_` will automatically be imported from the following locations:

1. `$XDG_CONFIG_HOME/updatemyip/providers`
1. `/etc/updatemyip/providers`
1. [sys.path](https://docs.python.org/3/library/sys.html#sys.path)

I'll write more documentation if people are interested, but for now, see the examples at [updatemyip/providers](updatemyip/providers) and [tests/providers](tests/providers).

### To Do

- Improve provider exception handling
- Add tests for built-in providers
