# Update My IP

Industrial-strength dynamic DNS client

## Features

- Extensible plugin-oriented architecture
- Built-in provider result validation
- Provider redundancy with optional retry and Fibonacci backoff
- Detailed logging
- Dry-run mode

### To Do

- Clean up argument parsing
- Improve provider error handling
- Add docs
- Add tests for built-in plugins?

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

FIXME: See [updatemyip/plugins](updatemyip/plugins) and [tests/plugins](tests/plugins) for now.
