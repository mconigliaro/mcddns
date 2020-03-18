# Update My IP

Work in progress towards an industrial-strength dynamic DNS client

## Features

- Extensibility via plugins
- Automatic address plugin result validation
- Plugin redundancy with optional retry and Fibonacci backoff
- Detailed logging
- Dry-run mode

### To Do

- Finalize plugin API, verify tests, etc.
- Add tests for built-in plugins?
- How to deal with required plugin options?

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

### Writing Plugins

FIXME: See [updatemyip/plugins](updatemyip/plugins) and [tests/plugins](updatemyip/plugins) for now.
