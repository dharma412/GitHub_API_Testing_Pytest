import os
import requests
import pytest


def pytest_addoption(parser):
    parser.addoption("--url", default='https://api.github.com')
    parser.addoption("--token", default="None")


@pytest.fixture(scope='session')
def github_session(request):
    print("I am running")
    token = request.config.getoption("--token")
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    session = requests.Session()
    session.headers.update(headers)
    session.base_url = request.config.getoption("--url")
    yield session
    session.close()