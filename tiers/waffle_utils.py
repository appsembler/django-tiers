from waffle import switch_is_active


REDIRECT_NON_AUTHENTICATED = 'tiers.redirect_non_authenticated'


def should_redirect_non_authenticated():
    return switch_is_active(REDIRECT_NON_AUTHENTICATED)
