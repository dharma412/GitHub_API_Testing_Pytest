import os
import requests
import pytest



@pytest.fixture()
def client():
    return os.getenv("GITHUB_TOKEN")

@pytest.fixture()
def getheader(client):
    return {"Authorization": f"token {client}"}

@pytest.fixture()
def github_session(getheader):
    session=requests.Session()
    session.headers.update(getheader)
    session.base_url=os.getenv("BASE_URL")
    yield session
    session.close()
