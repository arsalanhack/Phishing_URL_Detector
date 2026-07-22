import socket
from urllib.parse import urlparse


class URLValidator:

    @staticmethod
    def is_valid_url(url):
        try:
            parsed = urlparse(url)

            if not parsed.scheme:
                return False

            if not parsed.netloc:
                return False

            return True

        except Exception:
            return False

    @staticmethod
    def domain_exists(url):
        try:
            domain = urlparse(url).netloc

            if ":" in domain:
                domain = domain.split(":")[0]

            socket.gethostbyname(domain)
            return True

        except Exception:
            return False