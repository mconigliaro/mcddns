# Update My IP

Work in progress towards an industrial-strength dynamic DNS client

## Features

- Extensibility via plugins
- Plugin result validation
- Plugin redundancy (i.e. if the primary fails, use a backup)

### To Do

- Refactor plugin module and tests
- Add test for address plugin redundancy
  - Better logging?
  - Log attempt/retries?
- Add `is_hostname_private`/`is_hostname_global` and tests
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

FIXME

### Running Tests

    pytest

