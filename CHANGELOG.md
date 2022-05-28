# Change Log

## 1.2.0: 2022-05-28

- Use Poetry
- Require Python version `^3.8`
- Change provider subdirectory from `providers` to `provider`
- Add type annotations

## 1.1.2: 2021-02-17

- Improve exception logging

## 1.1.1: 2020-10-31

- Fix packaging error (`__init__.py` required to include providers)

## 1.1.0: 2020-10-31

- Don't require class methods in providers

## 1.0.0: 2020-06-23

- Make provider methods class methods (API change)
- Move provider utils into provider classes (API change)
- Fix bug where booleans were recognized as IP addresses
- Add `--cron` option

## 0.1.1: 2020-03-22

- Fix for pip not installing dependencies

## 0.1.0: 2020-03-22

- Initial public release
