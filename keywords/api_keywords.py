import logging
import os
import json
import random
import string
import time


def get_data_path(filename):
    return os.path.join(os.path.dirname(__file__), '..', 'Data', filename)

def load_repo_data(filepath):
    try:
        with open(filepath) as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return {}
    except json.JSONDecodeError:
        print(f"Invalid JSON in file: {filepath}")
        return {}


# def save_repo(filepath,generate_repo_name):
#     if os.path.exists(filepath):
#         data={}
#         if "repo_names" not in data or not isinstance(data['repo_names'],list):
#             data['repo_names']=[]
#         data['repo_names'].append(generate_repo_name)
#
#

def save_repo_name(file_path, random_string):
    """
    Append a generated repo name to the 'repo_name' list in a JSON file.
    Creates the file or key if they don't exist.
    """
    data = {}
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            pass
    data.setdefault("repo_name", []).append(random_string)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)



def fetch_repo(github_session, base_url):
    url = f"{base_url}/users/dharma412/repos"
    response = github_session.get(url,verify=False)
    if response.text:
        print(response.text)
    return response

def create_repo(github_session, base_url):
    repo_data = load_repo_data(get_data_path('test_data.json'))
    repo_data['name'] = repo_data['name'] + "".join((random.choice(string.ascii_letters + string.digits) for _ in range(6)))
    url = f'{base_url}/user/repos'
    response = github_session.post(url, json=repo_data,verify=False)
    if response.status_code != 201:
        print(f"GitHub API error: {response.status_code} - {response.text}")
    if response.status_code == 201:
        save_repo_name('../Data/repo_data.json', repo_data['name'])
    return response

def update_repo(github_session, base_url, max_retries=3, delay=5):
    update_data = load_repo_data(get_data_path('repo_data.json'))
    repo_names = update_data.get('repo_name', [])
    if not repo_names:
        print("No repo_name found in repo_data.json")
        return None
    old_repo = repo_names[-1]
    for attempt in range(max_retries):
        new_repo = old_repo + random.choice(string.ascii_letters)
        url = f"{base_url}/repos/dharma412/{old_repo}"
        payload = {'name': new_repo}
        print(f"[update_repo] Attempt {attempt+1}: old_repo='{old_repo}', new_repo='{new_repo}'")
        print(f"[update_repo] PATCH URL: {url}")
        print(f"[update_repo] Session headers: {github_session.headers}")
        if not old_repo or not isinstance(old_repo, str):
            print("[update_repo] ERROR: old_repo is empty or not a string!")
            return None
        logging.info(f"Updating repo: {old_repo} to {new_repo}")
        response = github_session.patch(url, json=payload)
        logging.error(response.text)
        if response.status_code == 200:
            save_repo_name('../Data/repo_data.json', new_repo)
            return response
        if response.status_code == 404:
            print(f"[update_repo] ERROR: Got 404 Not Found. URL: {url}, repo: {old_repo}")
        # Check for 422 and specific error message
        if response.status_code == 422 and 'conflicting repository operation' in response.text:
            print(f"GitHub 422 error: Conflicting operation in progress. Retrying in {delay} seconds...")
            time.sleep(delay)
        else:
            break
    print("Update failed after retries. Last response:", response.text)
    return response

def delete_repo(github_session,base_url):
    list_repos = load_repo_data(get_data_path('repo_data.json'))
    repo_names = list_repos.get('repo_name', [])
    last_response = None
    for repo in repo_names:
        url = f"{base_url}/repos/dharma412/{repo}"
        print(f"[delete_repo] DELETE URL: {url}")
        print(f"[delete_repo] Deleting repo: {repo}")
        print(f"[delete_repo] Session headers: {github_session.headers}")
        if not repo or not isinstance(repo, str):
            print("[delete_repo] ERROR: repo is empty or not a string!")
            continue
        last_response = github_session.delete(url)
        print(last_response.status_code)
        if last_response.status_code == 404:
            print(f"[delete_repo] ERROR: Got 404 Not Found. URL: {url}, repo: {repo}")
    return last_response
