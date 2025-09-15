import os
import requests
import pytest
from attr.converters import to_bool


@pytest.fixture(scope='session')
def github_session():
    print("I am running")
    header= {"Authorization": f"token {os.getenv('GITHUB_TOKEN')}"}
    session = requests.Session()
    session.headers.update(header)
    session.base_url = os.getenv("BASE_URL")
    yield session
    session.close()