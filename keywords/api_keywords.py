import os
import json
import json
from http.client import responses

def load_repo_data():
   with open("../Data/test_data.json") as f:
    return json.load(f)

def load_repo_data(filepath):
   with open(filepath) as f:
       return json.load(f)

def fetch_repo(github_session):
    response = github_session.get(os.getenv('BASE_URL')+'/users/Manjusha-1528/repos',verify=False)
    if response.text:
        print(response.text)
    return  response

def create_repo(github_session, repo_data=load_repo_data('../Data/test_data.json')):
    response = github_session.post(os.getenv('BASE_URL')+'/user/repos', json=repo_data,verify=False)
    return response

def update_repo(github_session, old_repo, update_data=load_repo_data('../Data/update_data.json')):
    url = f"{os.getenv('BASE_URL')}/repos/Manjusha-1528/{old_repo}"
    response = github_session.patch(url, json=update_data,verify=False)
    if response.text:
        print(response.text)
    return response

def delete_repo(github_session,delete_data=load_repo_data('../Data/delete_data.json')):
    response = github_session.delete(f"{os.getenv('BASE_URL')}+/repos/os.getenv('USER_NAME')/NewRepo")
    response=github_session.delete(url, json=delete_data,verify=False)
    return response