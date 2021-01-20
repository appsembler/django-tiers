from .app_settings import settings


def is_equal_or_sub_url(request_url, checked_url):
    """Stupidly simple method to check for URLs equality"""
    if request_url == checked_url:
        return True

    request_url = request_url.rstrip('/')
    checked_url = checked_url.rstrip('/')
    return request_url.startswith(checked_url)


def is_white_listed_url(url):
    """Checks if the URL is whitelisted for non-redirect."""
    if url == '/':
        # Homepage is not whitelisted.
        return False

    white_listed_urls = settings.redirect_white_list()
    if settings.expired_redirect_url():
        white_listed_urls.append(settings.expired_redirect_url())

    for white_listed_url in white_listed_urls:
        if is_equal_or_sub_url(request_url=url, checked_url=white_listed_url):
            return True

    return False
