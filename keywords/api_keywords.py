import logging
import os
import json
import random
import string
import time

# Set up module-level logger
logger = logging.getLogger(__name__)


def get_data_path(filename):
    return os.path.join(os.path.dirname(__file__), '..', 'Data', filename)

def load_repo_data(filepath):
    try:
        with open(filepath) as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        logger.error(f"File not found: {filepath}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Invalid JSON in file: {filepath}")
        return {}

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
            logger.warning(f"Invalid JSON in {file_path}, starting fresh.")
            pass
    data.setdefault("repo_name", []).append(random_string)
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)


def fetch_repo(github_session, base_url,username):
    url = f"{base_url}/users/{username}/repos"
    logger.info(f"Fetching repos from URL: {url}")
    response = github_session.get(url,verify=False)
    if response.text:
        logger.debug(response.text)
    return response

def create_repo(github_session, base_url,context):
    repo_data = load_repo_data(get_data_path('test_data.json'))
    logger.info(f"Original repo name: {repo_data['name']}")
    repo_data['name'] = repo_data['name'] + "".join((random.choice(string.ascii_letters + string.digits) for _ in range(6)))
    context['repo_name']=repo_data['name']
    url = f'{base_url}/user/repos'
    response = github_session.post(url, json=repo_data,verify=False)
    if response.status_code != 201:
        logger.error(f"GitHub API error: {response.status_code} - {response.text}")
    if response.status_code == 201:
        save_repo_name('Data/repo_data.json', repo_data['name'])
    return response

def update_repo(github_session, base_url,username, max_retries=3, delay=5):
    update_data = load_repo_data(get_data_path('repo_data.json'))
    repo_names = update_data.get('repo_name', [])
    if not repo_names:
        logger.error("No repo_name found in repo_data.json")
        return None
    old_repo = repo_names[-1]
    for attempt in range(max_retries):
        new_repo = old_repo + random.choice(string.ascii_letters)
        url = f"{base_url}/repos/{username}/{old_repo}"
        payload = {'name': new_repo}

        logger.info(f"[update_repo] Attempt {attempt+1}: old_repo='{old_repo}', new_repo='{new_repo}'")
        logger.debug(f"[update_repo] PATCH URL: {url}")

        if not old_repo or not isinstance(old_repo, str):
            logger.error("[update_repo] ERROR: old_repo is empty or not a string!")
            return None
        logger.info(f"Updating repo: {old_repo} to {new_repo}")
        response = github_session.patch(url, json=payload,verify=False)
        logger.error(response.text)
        if response.status_code == 200:
            save_repo_name('Data/repo_data.json', new_repo)
            return response
        if response.status_code == 404:
            logger.error(f"[update_repo] ERROR: Got 404 Not Found. URL: {url}, repo: {old_repo}")
        # Check for 422 and specific error message
        if response.status_code == 422 and 'conflicting repository operation' in response.text:
            logger.warning(f"GitHub 422 error: Conflicting operation in progress. Retrying in {delay} seconds...")
            time.sleep(delay)
        else:
            break
    logger.error(f"Update failed after retries. Last response: {response.text}")
    return response


def delete_repo(github_session, base_url,username):
    list_repos = load_repo_data(get_data_path('repo_data.json'))
    repo_names = list_repos.get('repo_name', [])
    logger.info(f"Repos to delete: {repo_names}")
    last_response = None
    for repo in repo_names:
        url = f"{base_url}/repos/{username}/{repo}"
        logger.info(f"[delete_repo] Checking repo: {repo}")

        check_response = github_session.get(url, verify=False)
        if check_response.status_code == 200:
            logger.info(f"[delete_repo] Repo {repo} exists. Deleting...")
            logger.debug(f"[delete_repo] DELETE URL: {url}")
            logger.debug(f"[delete_repo] Session headers: {github_session.headers}")
            last_response = github_session.delete(url, verify=False)
            logger.info(f"[delete_repo] Delete status: {last_response.status_code}")
            if last_response.status_code == 404:
                logger.error(f"[delete_repo] ERROR: Got 404 Not Found. URL: {url}, repo: {repo}")
        else:
            logger.warning(f"[delete_repo] Repo {repo} does not exist. Skipping.")
    return last_response


def create_empty_commit(github_session,base_url,username,context):
    repo_data = load_repo_data(get_data_path('commit_data.json'))
    check_response = github_session.put(f"{base_url}/repos/{username}/{context['repo_name']}/contents/README1.md",json=repo_data, verify=False)
    return check_response

def create_branch(github_session):
    pass
    # get sha  get_sha()
    # use this sha to create branch. create_branch()

