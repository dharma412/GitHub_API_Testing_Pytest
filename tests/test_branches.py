
import pytest
from keywords.branch_keywords import list_branches, get_branch ,rename_branch
from tests.conftest import send_branch_name

owner="dharma412"
repo="GitHub_API_Testing_Pytest"
branch_name="qa-manju"
new_name="QA-MANJU"

@pytest.mark.git
def test_list_branches(send_username, send_base_url,send_repo):
    branches=list_branches(send_repo,send_username)
    assert isinstance(branches,list)

@pytest.mark.git2
def test_get_branch(send_username,send_base_url,send_repo,send_branch_name):
    branch=get_branch(send_username,send_branch_name,send_repo)
    assert branch["name"] == send_branch_name

@pytest.mark.git3
def test_rename_branch(send_username,send_base_url,send_repo):
    response=rename_branch(send_username,send_repo,branch_name,new_name)
    assert response["name"]==new_name


