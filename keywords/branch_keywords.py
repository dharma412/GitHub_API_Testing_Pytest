import os
import requests

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json",
}

BASE_URL="https://api.github.com"


def list_branches(repo, owner):
    url=f"https://api.github.com/repos/{owner}/{repo}/branches"
    response=requests.get(url,headers=HEADERS)
    response.raise_for_status()
    return response.json()

def get_branch(owner, branch, repo):
    url=f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}"
    response=requests.get(url,headers=HEADERS)
    response.raise_for_status()
    return response.json()

def rename_branch(owner,repo,branch,new_name):
    url=f"https://api.github.com/repos/{owner}/{repo}/branches/{branch}/rename"
    payload = {"new_name": new_name}
    response=requests.post(url, headers=HEADERS, json=payload)
    response.raise_for_status()
    return response.json()