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


def list_branches(github_session, owner):
    url=f"https://api.github.com/repos/{owner}/{repo}/branches"
    response=requests.get(url,verify=False)
    response.raise_for_status()
    return response.json()

def get_branch(gith, branch, repo):
    url=f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}"
    response=requests.get(url,headers=HEADERS,verify=False)
    response.raise_for_status()
    return response.json()

def rename_branch(owner,repo,branch,new_name):
    url=f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}/rename"
    payload = {"new_name": new_name}
    response=requests.post(url, headers=HEADERS, json=payload,verify=False)
    response.raise_for_status()
    return response.json()