import logging
import os
import json
import random
import string


def load_repo_data(filepath):
    with open(filepath) as f:
        return json.load(f)

# def save_repo(filepath,generate_repo_name):
#     if os.path.exists(filepath):
#         data={}
#         if "repo_names" not in data or not isinstance(data['repo_names'],list):
#             data['repo_names']=[]
#         data['repo_names'].append(generate_repo_name)
#
#

def save_repo_name(file_path,random_string):
    """
    Generate a 6-character alphanumeric repo name,
    append it into 'repo_name' list in a JSON file,
    and return the generated repo name.

    If the file or key doesn't exist, it will create them.
    """
    # Generate random 6-character alphanumeric string


    # Load existing JSON or start fresh
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Ensure repo_name is a list
    if not isinstance(data.get("repo_name"), list):
        data["repo_name"] = []

    # Append new repo name (avoid duplicates if needed)
    data["repo_name"].append(random_string)

    # Save back to JSON
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)



def fetch_repo(github_session):
    response = github_session.get(github_session.base_url+'/users/dharma412/repos',verify=False)
    if response.text:
        print(response.text)
    return  response

def create_repo(github_session, repo_data=load_repo_data('../Data/test_data.json')):
    repo_data['name']=repo_data['name']+"".join((random.choice(string.ascii_letters + string.digits) for _ in range(6)))
    print(repo_data)
    response = github_session.post(os.getenv('BASE_URL')+'/user/repos', json=repo_data,verify=False)
    if response:
         (save_repo_name('../Data/repo_data.json',repo_data['name']))
    return response

def update_repo(github_session, update_data=load_repo_data('../Data/repo_data.json')):
    old_repo=update_data['repo_name'][-1]
    new_repo=old_repo+random.choice(string.ascii_letters)
    url = f"{os.getenv('BASE_URL')}/repos/dharma412/{old_repo}"
    date1={'name':new_repo}

    logging.error(new_repo)
    logging.info({'name':new_repo})
    response = github_session.patch(url, json=json.dumps({'name':new_repo}),verify=False)
    logging.error(response.text)
    if response:
        save_repo_name('../Data/repo_data.json',new_repo)
    return response

def delete_repo(github_session):
    list_repos =load_repo_data('../Data/repo_data.json')
    list_repos = list_repos['repo_name']
    for repo in list_repos:
        url = f"{os.getenv('BASE_URL')}/repos/dharma412/{repo}"
        response = github_session.delete(url, verify=False)
        print(response.status_code)