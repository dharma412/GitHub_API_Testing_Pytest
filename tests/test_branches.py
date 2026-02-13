import pytest
from keywords.api_keywords import create_repo, create_empty_commit


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
def get_sha(github_session,base_url):
    pass

def create_branch(github_session,base_url,username,context):
    pass