# Update My IP

Work in progress towards an industrial-strength dynamic DNS client

## Features

- Infinite extensibility via plugins
- Automatic address plugin result validation
- Plugin redundancy with optional retry and Fibonacci backoff
- Detailed logging
- Dry-run mode

### To Do

- Refactor plugin module and tests
- Add test for address plugin redundancy
- Add tests for built-in plugins
- How to determine default plugins?
- How to deal with required plugin options?

## Running the Application

    updatemyip

Use `--help` to see available options.

## Development

### Getting Started

    pip install pipenv
    pipenv install --dev
    pipenv shell
    ...

### Writing Plugins

FIXME: See [updatemyip/plugins](updatemyip/plugins) for now.

### Running Tests

    pytest
