import requests


def http_adapter():
    adapter = requests.adapters.HTTPAdapter(max_retries=3)

    return adapter


def create_session():
    session = requests.Session()

    return session
