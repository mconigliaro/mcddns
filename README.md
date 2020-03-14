# Update My IP

Testing ideas for a better DDNS client

## Planned Features

- Extensibility via plugins
- Plugin redundancy (i.e. if the primary fails, use a backup)
- Use result from fastest plugin

## Running the Application

    updatemyip

Use `--help` to see available options.

## Development

### Getting Started

    pip install pipenv
    pipenv install --dev
    pipenv shell
    ...

### To Do

- Add tests
- Better error handling
- Finalize plugin API
