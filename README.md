# Update My IP

Testing ideas for a better DDNS client

## Planned Features

- Extensibility via plugins
- Plugin redundancy (i.e. if the primary fails, use a backup)

## Running the Application

    updatemyip

Use `--help` to see available options.

## Development

### Getting Started

    pip install pipenv
    pipenv install --dev
    pipenv shell
    ...

### Running Tests

    pytest

### To Do

- Handle data validation errors
- Add tests for built-in plugins
- How to deal with required plugin options?
