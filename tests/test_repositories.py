import pytest
from  keywords.api_keywords import *


@pytest.mark.git
def test_fetch_user_repo_data(github_session):
    response= fetch_repo(github_session)
    assert response.status_code==200

@pytest.mark.git2
def test_create_repo(github_session):
    response = create_repo(github_session)
    print(response.status_code)
    assert response.status_code == 201

def test_update_repo(github_session):
    response = update_repo(github_session)
    assert response.status_code == 200

def test_delete_repo(github_session):
    response = delete_repo(github_session)
    assert response.status_code==204