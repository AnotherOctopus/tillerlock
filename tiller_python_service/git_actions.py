from git import Repo, GitCommandError
import subprocess
import tempfile
import uuid
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
    repo_name = url.split("/")[-1].replace(".git", "")
    full_repo_path = os.path.join(target_dir, repo_name)

    result = subprocess.run(["git", "clone", url, full_repo_path], capture_output=True, text=True)

    if result.returncode != 0:
        print(f"Error cloning the repository. Return code: {result.returncode}")
        print(result.stderr)
        return None

    return full_repo_path

def git_add_all(repo_path):
    try:
        repo = Repo(repo_path)
        repo.index.add("*")
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

def generate_random_branch_name():
    """
    Generate a random branch name.

    Returns:
        str: The generated branch name.
    """
    return "branch-" + str(uuid.uuid4())

def clone_and_create_new_branch(repo_url, initial_branch):
    """
    Clone a repository, switch to a specified branch, and create a new branch with a random name.

    Examples:
        branch = clone_and_create_new_branch("git@github.com:AnotherOctopus/tillerlock.git", "git-functions")

    Parameters:
        repo_url (str): The URL of the git repository.
        initial_branch (str): The name of the branch to switch to after cloning.

    Returns:
        str: A message about the operation's success or the error message.
    """
    # Clone the repo
    repo_path = clone_repo(repo_url)
    if repo_path is None:
        return "Failed to clone repository"

    # Switch to the initial branch
    checkout_message = git_checkout_branch(repo_path, initial_branch)
    if not checkout_message.startswith("Switched"):
        return "Failed to switch to initial branch: " + checkout_message

    # Create a new branch with a random name and switch to it
    new_branch_name = generate_random_branch_name()
    try:
        repo = Repo(repo_path)
        repo.git.checkout('-b', new_branch_name)
        return "Switched to new branch: " + new_branch_name
    except GitCommandError as e:
        return "Failed to switch to new branch: " + str(e)

def git_add_commit_push(repo_path, commit_message):
    """
    Add all changes, commit them, and push to the remote repository.

    Parameters:
        repo_path (str): The full path to the local git repository.
        commit_message (str): The commit message.

    Returns:
        str: A message about the operation's success or the error message.
    """
    # Add all changes
    add_message = git_add_all(repo_path)
    if not add_message.startswith("All files"):
        return "Failed to add changes: " + add_message

    # Commit changes
    commit_message = git_commit(repo_path, commit_message)
    if not commit_message.startswith("Commit"):
        return "Failed to commit changes: " + commit_message

    # Push changes
    current_branch = Repo(repo_path).active_branch.name
    push_message = git_push(repo_path, current_branch)
    if not push_message.startswith("Push"):
        return "Failed to push changes: " + push_message

    return "Add, commit, and push operations were successful"