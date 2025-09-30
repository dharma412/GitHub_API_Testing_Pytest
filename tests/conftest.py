import os
import requests
import pytest
import json
from pygments.lexer import default

#Test

def pytest_addoption(parser):
    parser.addoption("--url", default=os.getenv('BASE_URL', 'https://api.github.com'))
    parser.addoption("--token", default=None)
    parser.addoption("--user_name", default="dharma412")

@pytest.fixture(scope='session')
def github_session(request):
    print("I am running")
    token = request.config.getoption("--token")
    headers = {}
    if token:
        headers["Authorization"] = f"token {token}"
    session = requests.Session()
    session.headers.update(headers)
    yield session
    print("end of testcase")
    session.close()
    clear_repo_data()

def clear_repo_data():
    with open('../Data/repo_data.json', 'w') as f:
        json.dump({"repo_name": []}, f)

@pytest.fixture(scope='session')
def base_url(request):
    return request.config.getoption("--url")

@pytest.fixture(scope='session')
def username(request):
    return request.config.getoption("--user_name")