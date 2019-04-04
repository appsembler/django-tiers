# Django Tiers

[![Build Status](https://travis-ci.org/appsembler/django-tiers.svg?branch=master)](https://travis-ci.org/appsembler/django-tiers)
[![codecov](https://codecov.io/gh/appsembler/django-tiers/branch/master/graph/badge.svg)](https://codecov.io/gh/appsembler/django-tiers)

This should serve as a reusable django app for representing tiers. Currently it only implements the
"Trial" tier but it should be easily extendable.

## Install

Add `tiers` to `INSTALLED_APPS`.

Set `TIERS_EXPIRED_REDIRECT_URL` and `TIERS_ORGANIZATION_MODEL` in settings. Run `manage.py migrate`.

Add `tiers.middleware.TierMiddleware` to MIDDLEWARE in settings.py.
You might want to add it at the top.

## Testing

    mkvirtualenv django-tiers
    make install-dev
    make install-test-deps
    py.test

