# Update My IP

[![updatemyip](https://circleci.com/gh/mconigliaro/updatemyip.svg?style=svg)](https://circleci.com/gh/mconigliaro/updatemyip)

Industrial-strength dynamic DNS client

## Features

- Extensible plugin-oriented architecture with a simple API
    - Address providers are responsible for obtaining an address
    - DNS providers are responsible for managing a DNS record
- Address provider features:
    - Built-in result validation
    - Optionally use multiple providers (keep trying until one succeeds)
- All provider features:
    - Optional retry with Fibonacci backoff
    - Detailed logging
    - Dry-run mode

### Built-In Providers

#### Address Providers

- `aws.CheckIP`: Obtains a public IPv4 address via [Amazon Web Services](https://aws.amazon.com/)
- `dyn.CheckIP`: Obtains a public IPv4 address via [Dyn](https://dyn.com/)
- `google.CheckIP`: Obtains a public IPv4 address via [Google Domains](https://domains.google.com)
- `ipify.IPv4`: Obtains a public IPv4 address via [ipify](https://www.ipify.org/)
- `ipify.IPv6`: Obtains an IPv6 address via [ipify](https://www.ipify.org/)

#### DNS Providers

- `aws.Route53`: Manages records in [Amazon Route53](https://aws.amazon.com/route53/)

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

A provider is any class that inherits from `AddressProvider` or `DNSProvider`. In production mode, Python modules/packages prefixed with `updatemyip_` will automatically be imported from the following locations:

1. `$XDG_CONFIG_HOME/updatemyip/providers`
1. `/etc/updatemyip/providers`
1. [sys.path](https://docs.python.org/3/library/sys.html#sys.path)

Example: If you create a file at `$XDG_CONFIG_HOME/updatemyip/providers/updatemyip_foo.py` with a class named `Bar` that inherits from one of the `Provider` subclasses, your module can be referenced (e.g. in command-line options) as `foo.Bar`.

#### Provider Methods

Each provider type has a set of methods that will be called in a particular order. Note that some of these methods are expected to return a specific value in order to progress to the next step.

##### All Providers

1. `options_pre(parser)`: Runs before option parsing. Use this method to add your own provider-specific command line arguments (See: [argparse](https://docs.python.org/3.6/library/argparse.html)).
1. `options_post(parser, options)`: Runs after option parsing. Use this method to do things with your provider-specific command line arguments.

##### Address Providers

1. `fetch(options)`: Fetches and returns an IP address, hostname, etc.
1. `validate(options, address)`: Returns `True` if the address is valid and `False` otherwise

##### DNS Providers

1. `check(options, address)`: Returns `True` if a DNS update is required and `False` otherwise
1. `update(options, address)`: Returns `True` if a DNS update was successful and `False` otherwise

#### Examples

I'll write more documentation if people are interested, but for now, see the examples at [updatemyip/providers](updatemyip/providers) and [tests/providers](tests/providers).

#### Releases

1. Bump `VERSION` in [updatemyip/meta.py](updatemyip/meta.py)
1. Update [CHANGELOG.md](CHANGELOG.md)
1. Run `release` script:
    ```
    release <version>
    ```

### To Do

- Add tests for built-in providers
