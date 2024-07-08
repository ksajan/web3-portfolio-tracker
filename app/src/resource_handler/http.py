import requests
from requests.adapters import HTTPAdapter, Retry


def create_http_adapter():
    retry_strategy = Retry(
        total=10,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["HEAD", "GET", "OPTIONS"],
        backoff_factor=0.1,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    return adapter


def create_session():
    session = requests.Session()
    adapter = create_http_adapter()
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session
