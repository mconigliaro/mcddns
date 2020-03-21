# Update My IP

Industrial-strength dynamic DNS client

## Features

- Extensible plugin-oriented architecture
- Built-in provider result validation
- Provider redundancy with optional retry and Fibonacci backoff
- Detailed logging
- Dry-run mode

### To Do

- How to determine default address providers?
- Add version info for providers
- Improve provider exception handling
- Add docs
- Add tests for built-in providers?

## Installation

FIXME

## Development

### Getting Started

    pip install pipenv
    pipenv install --dev
    pipenv shell
    ...

### Running Tests

    pytest

## Running the Application

Use `--help` to see available options.

    updatemyip

### Writing Providers

FIXME: See [updatemyip/providers](updatemyip/providers) and [tests/providers](tests/providers) for now.
