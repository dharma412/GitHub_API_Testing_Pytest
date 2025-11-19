import os
import requests
import pytest
import json


def pytest_addoption(parser):
    parser.addoption("--url", default=os.getenv('BASE_URL', 'https://api.github.com'))
    parser.addoption("--token", default=None)
    parser.addoption("--username", default="dharma412")
    parser.addoption("--repo", default="GitHub_API_Testing_Pytest")
    parser.addoption("--branch_name", default="qa-manju")
    parser.addoption("--new_name", default="qa-newmanju")


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

    with open('Data/repo_data.json', 'w') as f:
        json.dump({"repo_name": []}, f)


@pytest.fixture(scope='session')
def github_base_url(request):
    return request.config.getoption("--url")


@pytest.fixture(scope='session')
def github_username(request):
    return request.config.getoption("--username")


@pytest.fixture(scope='session')
def send_repo(request):
    return request.config.getoption("--repo")


@pytest.fixture(scope='session')
def send_branch_name(request):
    return request.config.getoption("--branch_name")


@pytest.fixture(scope='session')
def send_new_name(request):
    return request.config.getoption("--new_name")
