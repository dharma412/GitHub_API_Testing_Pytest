import pytest
from keywords.repo_keywords import  *
from keywords.repo_keywords import create_repo, create_empty_commit
from keywords.branch_keywords import *


@pytest.mark.branch
def test_create_repo(github_session,base_url,context):
    response = create_repo(github_session,base_url,context)
    print(response.status_code)
    assert response.status_code == 201

@pytest.mark.branch
def test_commit_on_repo(github_session,base_url,username,context):
    responses= create_empty_commit(github_session,base_url,username,context)
    assert responses.status_code == 201

@pytest.mark.branch
def test_get_sha_id(github_session,base_url,username,context):
    responses = get_sha_id(github_session,base_url,username,context)
    print(responses)

@pytest.mark.branch
def test_create_branch(github_session,base_url,username,context):
    responses= create_branch(github_session,base_url,username,context)
    assert responses.status_code == 201