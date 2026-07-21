import re
import socket
import ssl

import requests

from bs4 import BeautifulSoup
from urllib.parse import urlparse



class FeatureExtractor:

    def __init__(self):
        pass

    # ==========================================================
    # 1. Having IP Address
    # ==========================================================

    def having_ip_address(self, url):

        hostname = urlparse(url).hostname or ""

        ip_pattern = re.compile(
            r"^(?:\d{1,3}\.){3}\d{1,3}$"
        )

        if ip_pattern.match(hostname):
            return -1

        return 1

    # ==========================================================
    # 2. URL Length
    # ==========================================================

    def url_length(self, url):

        length = len(url)

        if length < 54:
            return 1

        elif length <= 75:
            return 0

        else:
            return -1

    # ==========================================================
    # 3. Having @ Symbol
    # ==========================================================

    def having_at_symbol(self, url):

        if "@" in url:
            return -1

        return 1

    # ==========================================================
    # 4. Double Slash Redirecting
    # ==========================================================

    def double_slash_redirecting(self, url):

        position = url.rfind("//")

        if position > 7:
            return -1

        return 1

    # ==========================================================
    # 5. Prefix-Suffix
    # ==========================================================

    def prefix_suffix(self, url):

        hostname = urlparse(url).hostname or ""

        if "-" in hostname:
            return -1

        return 1

    # ==========================================================
    # 6. Having Sub Domain
    # ==========================================================

    def having_sub_domain(self, url):

        hostname = urlparse(url).hostname or ""

        hostname = hostname.replace("www.", "")

        dots = hostname.count(".")

        if dots == 1:
            return 1

        elif dots == 2:
            return 0

        else:
            return -1

    # ==========================================================
    # 7. Shortening Service
    # ==========================================================

    def shortening_service(self, url):

        hostname = (urlparse(url).hostname or "").lower()

        shortening_services = [
            "bit.ly",
            "goo.gl",
            "tinyurl.com",
            "ow.ly",
            "t.co",
            "is.gd",
            "buff.ly",
            "adf.ly",
            "cutt.ly",
            "rebrand.ly",
            "shorturl.at",
            "tiny.cc"
        ]

        for service in shortening_services:
            if service in hostname:
                return -1

        return 1

    # ==========================================================
    # 8. DNS Record
    # ==========================================================

    def dns_record(self, url):

        hostname = urlparse(url).hostname

        if not hostname:
            return -1

        try:
            socket.gethostbyname(hostname)
            return 1

        except socket.gaierror:
            return -1
    # ==========================================================
    # 9. SSL Final State
    # ==========================================================

    def ssl_final_state(self, url):

        parsed = urlparse(url)

        hostname = parsed.hostname

        if parsed.scheme != "https":
            return -1

        try:

            context = ssl.create_default_context()

            with socket.create_connection((hostname, 443), timeout=5) as sock:

                with context.wrap_socket(sock, server_hostname=hostname):

                    return 1

        except Exception:
            return -1  
        
        # ==========================================================
        # Extract Features
        # ==========================================================
# ==========================================================
# 10. HTTPS Token
# ==========================================================

    def https_token(self, url):

        hostname = (urlparse(url).hostname or "").lower()

        hostname = hostname.replace("www.", "")

        if "https" in hostname:
            return -1

        return 1

# ==========================================================
# 11. URL of Anchor
# ==========================================================

    def url_of_anchor(self, url):

        try:

            response = requests.get(url, timeout=5)

            soup = BeautifulSoup(response.text, "html.parser")

            anchors = soup.find_all("a")

            if len(anchors) == 0:
                return 1

            unsafe = 0

            for anchor in anchors:

                href = anchor.get("href")

                if not href:
                    unsafe += 1

                elif href.startswith("#"):
                    unsafe += 1

                elif href.lower().startswith("javascript"):
                    unsafe += 1

            ratio = unsafe / len(anchors)

            if ratio < 0.31:
                return 1

            elif ratio <= 0.67:
                return 0

            else:
                return -1

        except Exception:

            return -1

    def extract_features(self, url):

        return [

        self.having_ip_address(url),

        self.url_length(url),

        self.having_at_symbol(url),

        self.double_slash_redirecting(url),

        self.prefix_suffix(url),

        self.having_sub_domain(url),

        self.ssl_final_state(url),

        self.https_token(url),

        self.shortening_service(url),

        self.dns_record(url),

        self.url_of_anchor(url)

    ]