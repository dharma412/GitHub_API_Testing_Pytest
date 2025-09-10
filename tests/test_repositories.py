import pytest
from  keywords.api_keywords import *


@pytest.mark.git
def test_fetch_user_repo_data(github_session):
    response= fetch_repo(github_session)
    assert response.status_code==200

@pytest.mark.git2
def test_create_repo(github_session):
    repo_data = {
        "name": "test-repo11",
        "description": "Created via API",
        "private": False
    }
    response = create_repo(github_session, repo_data)
    assert response.status_code == 201


# def test_update_repo(github_session):
#     owner = "dharma412"
#     repo = "test-repo"
#     update_data = {
#         "description": "Updated description"
#     }
#     response = update_repo(github_session, owner, repo, update_data)
#     assert response.status_code == 200


# def test_delete_repo():
#     pass