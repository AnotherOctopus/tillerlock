import pathlib
import requests
from static_vals import GITHUB_TOKEN, REPO_NAME, OWNER
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

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
    retry_strategy = Retry(
        total=3,
        status_forcelist=[429, 500, 502, 503, 504],
        method_whitelist=["GET"],
        backoff_factor=1
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount("https://", adapter)
    response = session.get(url, headers=headers)
    return response.json()
