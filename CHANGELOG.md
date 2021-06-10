# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.2.4] - 2021-06-10

 - Add more details when a tier error happens in the middleware
 - Django 2: Add `app_label` to the Django models
 - Python 3: Convert `__unicode__` to `__str__`

## [0.2.3] - 2021-01-20

 - Support expired URL redirect for non-authenticated users (needs the [Waffle Switch](https://waffle.readthedocs.io/en/stable/types/switch.html) `tiers.redirect_non_authenticated` to be switched on).
 - Improved whitelisted urls
 - Added and refactored tests for expired tiers

## [0.2.2] - 2020-09-25

 - Remove setup.py package restrictions (fixes appsembler/devstack#50)

## [0.2.1] - 2020-09-09

- Added a missing migration

## [0.2.0] - 2020-07-16

- Added basic honeycomb instrumentation to middleware
- Removed a Django 2 deprecation warning
- Added testing against Python 3.8
- Added testing against Django 2.x

## [0.1.0] - 2020-06-04

### Changed

- Added supoort for Django 1.10+ style middleware

## [0.0.20] - 2019-11-06

- starting changelog

[unreleased]: https://github.com/appsembler/django-tiers/compare/v0.2.3...HEAD
[0.2.3]: https://github.com/appsembler/django-tiers/compare/v0.2.2...v0.2.3
[0.2.2]: https://github.com/appsembler/django-tiers/compare/v0.2.1...v0.2.2
[0.2.1]: https://github.com/appsembler/django-tiers/compare/v0.2.0...v0.2.1
[0.2.0]: https://github.com/appsembler/django-tiers/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/appsembler/django-tiers/compare/v0.0.20...v0.1.0
[0.0.20]: https://github.com/appsembler/django-tiers/releases/tag/v0.0.20
