import os
import requests
import pytest


def pytest_addoption(parser):
    parser.addoption("--url", default=os.getenv('BASE_URL', 'https://api.github.com'))
    parser.addoption("--token", default=None)



@pytest.fixture(scope='function')
def github_session(request):
    print("I am running")
    token = request.config.getoption("--token")
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    session = requests.Session()
    session.headers.update(headers)
    yield session
    session.close()