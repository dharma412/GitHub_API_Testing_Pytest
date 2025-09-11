import os
import json

def load_repo_data(filepath):
    with open(filepath) as f:
        return json.load(f)

def fetch_repo(github_session):
    response = github_session.get(os.getenv('BASE_URL')+'/users/dharma412/repos',verify=False)
    if response.text:
        print(response.text)
    return  response

def create_repo(github_session, repo_data=load_repo_data('../Data/test_data.json')):
    response = github_session.post(os.getenv('BASE_URL')+'/user/repos', json=repo_data,verify=False)
    return response

def update_repo(github_session,old_repo, update_data=load_repo_data('../Data/update_repo_data.json')):
    url = f"{os.getenv('BASE_URL')}/repos/dharma412/{old_repo}"
    response = github_session.patch(url, json=update_data,verify=False)
    return response