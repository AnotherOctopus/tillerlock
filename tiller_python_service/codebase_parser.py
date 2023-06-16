import pathlib
import requests
from static_vals import GITHUB_TOKEN, REPO_NAME, OWNER

CODE_EXTENSIONS = [".py", ".rs"]


def parse(path):
    for file_path in path.rglob(f"*[{'|'.join(CODE_EXTENSIONS)}]"):
        if file_path.is_file() and "__" not in str(file_path):
            with open(file_path, "r") as f:
                yield f.read()


def call_gh_api_for_pr_info(pr_number):
    """
    Call the GitHub API to get information about a pull request.

    Parameters:
        pr_number (int): The number of the pull request.

    Returns:
        dict: The response from the GitHub API.
    """
    url = f"https://api.github.com/repos/{OWNER}/{REPO_NAME}/pulls/{pr_number}"
    headers = {"Authorization": f"token {GITHUB_TOKEN}"}
    response = requests.get(url, headers=headers)
    return response.json()