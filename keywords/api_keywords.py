import os

def fetch_repo(github_session):
    response = github_session.get(os.getenv('BASE_URL')+'/users/dharma412/repos',verify=False)
    return  response


def create_repo(github_session, repo_data):
    response = github_session.post(os.getenv('BASE_URL')+'/user/repos', json=repo_data,verify=False)
    return response

def update_repo(github_session, owner, repo, update_data):
    url = f"{github_session.base_url}/repos/{owner}/{repo}"
    response = github_session.patch(url, json=update_data)
    return response

