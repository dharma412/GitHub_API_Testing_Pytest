import os
import requests

# GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
#
# HEADERS = {
#     "Authorization": f"token {GITHUB_TOKEN}",
#     "Accept": "application/vnd.github+json",
# }
#
# BASE_URL="https://api.github.com"


def list_branches(github_session, base_url,username,context):
    url=f"https://api.github.com/repos/{username}/{repo}/branches"
    response=requests.get(url,verify=False)
    response.raise_for_status()
    return response.json()

def get_branch(github_session, branch, base_url,username,contextrepo):
    url=f"https://api.github.com/repos/{username}/{repo}/branches/{branch}"
    response=requests.get(url,headers=HEADERS,verify=False)
    response.raise_for_status()
    return response.json()

def rename_branch(github_session, branch, base_url,username,contextrepo):
    url=f"https://api.github.com/repos/{username}/{repo}/branches/{branch}/rename"
    payload = {"new_name": new_name}
    response=requests.post(url, headers=HEADERS, json=payload,verify=False)
    response.raise_for_status()
    return response.json()

def get_sha_id(github_session,base_url,username,context):
    check_response= github_session.get(f"{base_url}/repos/{username}/{context['repo_name']}/git/ref/heads/main", verify=False)
    if check_response.status_code == 200:
        context['sha']=(check_response.json().get("object", {}).get("sha"))
    return context['sha']

def create_branch(github_session):
    pass
    # get sha  get_sha()
    # use this sha to create branch. create_branch()
