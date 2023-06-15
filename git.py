from git import Repo, GitCommandError
import subprocess
import tempfile
import os

def clone_repo(url):
    """
    Clone a git repository from a specified URL into a randomly named directory within /tmp.

    Parameters:
        url (str): The URL of the git repository.

    Returns:
        str: The full path to the cloned repository.
    """
    # Create a temporary directory.
    target_dir = tempfile.mkdtemp(dir="/tmp")
    # Clone the repository.
    subprocess.Popen(["git", "clone", url, target_dir], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    repo_name = url.split("/")[-1].replace(".git", "")
    full_repo_path = os.path.join(target_dir, repo_name)
    return full_repo_path

def git_add_all(repo_path):
    try:
        repo = Repo(repo_path)
        repo.git.add(A=True)  # Adds all changes
        return "All files added successfully"
    except GitCommandError as e:
        return str(e)

def git_commit(repo_path, message):
    try:
        repo = Repo(repo_path)
        repo.index.commit(message)
        return "Commit successful with message: {}".format(message)
    except GitCommandError as e:
        return str(e)

def git_push(repo_path, branch='master'):
    try:
        repo = Repo(repo_path)
        origin = repo.remote(name='origin')
        origin.push(branch)
        return "Push to {} successful".format(branch)
    except GitCommandError as e:
        return str(e)

def git_fetch_all(repo_path):
    try:
        repo = Repo(repo_path)
        for remote in repo.remotes:
            remote.fetch()
        return "Fetch all successful"
    except GitCommandError as e:
        return str(e)

def git_checkout_branch(repo_path, branch_name):
    try:
        repo = Repo(repo_path)
        repo.git.checkout(branch_name)
        return "Switched to branch: {}".format(branch_name)
    except GitCommandError as e:
        return str(e)

