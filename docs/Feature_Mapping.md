# Feature Mapping

**Project:** PhishGuard AI – Phishing URL Detector

## Purpose

This document defines the machine learning features used throughout the project.

Every selected feature must satisfy two conditions:

1. It exists in the training dataset.
2. It can be extracted from a live URL during prediction.

This document is the single source of truth for:

- Google Colab training notebook
- Flask Feature Extractor
- Predictor module

---

## Selected Features

| Feature | Dataset Attribute | Dataset Values | Description | Extraction Method | Python Library | Status |
|----------|-------------------|---------------|-------------|-------------------|----------------|--------|
| IP Address | having_IP_Address | {-1, 1} | Detects whether the URL uses an IP address instead of a domain name. | Regular Expression | re | Pending |
| URL Length | URL_Length | {-1, 0, 1} | Determines whether the URL length is suspicious. | Count URL characters | Built-in | Pending |
| Having @ Symbol | having_At_Symbol | {-1, 1} | Checks whether '@' exists in the URL. | String search | Built-in | Pending |
| Redirecting | double_slash_redirecting | {-1, 1} | Detects extra '//' used for redirection. | String search | Built-in | Pending |
| Prefix/Suffix | Prefix_Suffix | {-1, 1} | Checks whether the domain contains '-'. | Domain parsing | urllib.parse | Pending |
| Subdomain | having_Sub_Domain | {-1, 0, 1} | Counts the number of subdomains. | Domain parsing | urllib.parse | Pending |
| SSL Final State | SSLfinal_State | {-1, 0, 1} | Determines whether the SSL certificate is valid. | SSL certificate inspection | ssl, socket | Pending |
| HTTPS Token | HTTPS_token | {-1, 1} | Detects fake "https" inside the domain name. | Domain parsing | urllib.parse | Pending |
| Shortening Service | Shortining_Service | {-1, 1} | Detects known URL shortening services. | Compare against known shortener list | re | Pending |
| DNS Record | DNSRecord | {-1, 1} | Checks whether a DNS record exists for the domain. | DNS lookup | socket | Pending |
| URL Anchor | URL_of_Anchor | {-1, 0, 1} | Measures suspicious anchor tags within the webpage. | HTML parsing | requests, BeautifulSoup | Pending |

---

## Selected Python Libraries

- pandas
- numpy
- scipy
- xgboost
- lightgbm
- scikit-learn
- joblib
- requests
- beautifulsoup4
- urllib
- socket
- ssl
- re

---

## Project Status

- [x] Feature Selection
- [x] Dataset Validation
- [ ] Google Colab Training Notebook
- [ ] Model Evaluation
- [ ] Save Trained Models
- [ ] Feature Extractor
- [ ] Flask Integration
- [ ] Testing