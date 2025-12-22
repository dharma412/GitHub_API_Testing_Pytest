import pytest
from  keywords.api_keywords import *

#this
@pytest.mark.sample
def test_fetch_user_repo_data(github_session, base_url,username):
    result = fetch_repo(github_session, base_url,username)
    assert result.status_code==200

@pytest.mark.e2e
@pytest.mark.dependency(name="create_repo")
def test_create_repo(github_session,base_url,context):
    response = create_repo(github_session,base_url,context)
    print(response.status_code)
    assert response.status_code == 201

@pytest.mark.e2e
@pytest.mark.dependency(depends=["create_repo"])
def test_commit_on_repo(github_session,base_url,username,context):
    responses= create_empty_commit(github_session,base_url,username,context)
    assert responses.status_code == 201


    # create branch - automation from main

    # push code to automation



@pytest.mark.git2
def test_update_repo(github_session,base_url,username):
    response = update_repo(github_session,base_url,username)
    assert response.status_code == 200
#
# @pytest.mark.git2
# def test_delete_repo(github_session,base_url,username):
#     response = delete_repo(github_session,base_url,username)
#     assert response.status_code==204

# create repo -- repo--> repo_data.py update



