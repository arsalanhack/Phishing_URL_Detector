from urllib.parse import urlparse

def validate_url(url):

    try:
        parsed = urlparse(url)

        return bool(parsed.scheme and parsed.netloc)

    except Exception:

        return False