import pytest
from  keywords.api_keywords import *

@pytest.mark.repo
def test_fetch_user_repo_data(github_session, base_url,username):
    result = fetch_repo(github_session, base_url,username)
    assert result.status_code==200

@pytest.mark.e2e
@pytest.mark.repo
def test_create_repo(github_session,base_url,context):
    response = create_repo(github_session,base_url,context)
    print(response.status_code)
    assert response.status_code == 201

@pytest.mark.git2
def test_update_repo(github_session,base_url,username):
    response = update_repo(github_session,base_url,username)
    assert response.status_code == 200

@pytest.mark.git2
def test_delete_repo(github_session,base_url,username):
    response = delete_repo(github_session,base_url,username)
    assert response.status_code==204



