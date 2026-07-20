class FeatureExtractor:

    def extract(self, url):

        features = {
            "https": self.has_https(url),
            "ip": self.has_ip(url),
            "at_symbol": self.has_at(url),
            "subdomains": self.count_subdomains(url),
            "shortener": self.is_shortened(url),
            "length": self.url_length(url),
            "digits": self.count_digits(url),
            "hyphen": self.has_hyphen(url),
            "dots": self.count_dots(url)
        }

        return features