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

- `aws.CheckIP`: https://checkip.amazonaws.com/
- `dyn.CheckIP`: http://checkip.dyndns.com/
- `google.CheckIP`: https://domains.google.com/checkip
- `ipify.Ipv4`: https://api.ipify.org/
- `ipify.Ipv6`: https://api6.ipify.org/

#### DNS

DNS providers are responsible for managing DNS records.

- `aws.Route53`: Manages [Route53](https://aws.amazon.com/route53/) DNS records

## Installation

FIXME

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

In production mode, Python modules/packages prefixed with `updatemyip_` will automatically be loaded from the following locations:

1. `$XDG_CONFIG_HOME/updatemyip/providers`
1. `/etc/updatemyip/providers`
1. [updatemyip/providers](updatemyip/providers)

FIXME: Need more docs

### To Do

- Improve provider exception handling
- Add tests for built-in providers
