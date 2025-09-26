import pytest
from  keywords.api_keywords import *


@pytest.mark.git
def test_fetch_user_repo_data(github_session, base_url,username):
    response = fetch_repo(github_session, base_url,username)
    assert response.status_code==200

@pytest.mark.git2
def test_create_repo(github_session,base_url):
    response = create_repo(github_session,base_url)
    print(response.status_code)
    assert response.status_code == 201

@pytest.mark.git2
def test_update_repo(github_session,base_url,username):
    response = update_repo(github_session,base_url,username)
    assert response.status_code == 200
#
@pytest.mark.git2
def test_delete_repo(github_session,base_url,username):
    response = delete_repo(github_session,base_url,username)
    assert response.status_code==204

# create repo -- repo--> repo_data.py update



