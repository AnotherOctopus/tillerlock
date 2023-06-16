from git import Repo, GitCommandError
import git
import logging
from static_vals import GITHUB_TOKEN 
import subprocess
import tempfile
import uuid
import requests
import json
import os
import re
import openai

logging.basicConfig(filename='example.log', level=logging.INFO)

def my_sorting_function(arr):
    n = len(arr)
    # optimize code, so if the array is already sorted, it doesn't need
    # to go through the entire process
    swapped = False
    # Traverse through all array elements
    for i in range(n-1):
        # range(n) also work but outer loop will
        # repeat one time more than needed.
        # Last i elements are already in place
        for j in range(0, n-i-1):
 
            # traverse the array from 0 to n-i-1
            # Swap if the element found is greater
            # than the next element
            if arr[j] > arr[j + 1]:
                swapped = True
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
         
        if not swapped:
            # if we haven't needed to make a single swap, we
            # can just exit the main loop.
            return

def new_but_terribly_misguided_function(a) -> int:
    sorted_list = my_sorting_function(a)
    logging.info(sorted_list)
    return sorted_list[0] + sorted_list[1]


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
    clone_url = url.replace("https://", f"https://x-access-token:{GITHUB_TOKEN}@")
    result = subprocess.run(["git", "clone", clone_url, full_repo_path])

    if result.returncode != 0:
        logging.error(f"Error cloning the repository. Return code: {result.returncode}")
        return None
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
        branch_name, repo_path = clone_and_create_new_branch("git@github.com:AnotherOctopus/tillerlock.git", "git-functions")

    Parameters:
        repo_url (str): The URL of the git repository.
        initial_branch (str): The name of the branch to switch to after cloning.

    Returns:
        tuple: A tuple containing the branch name and repo path. If an error occurs, returns an error message.
    """
    # Clone the repo
    repo_path = clone_repo(repo_url)
    if repo_path is None:
        logging.error("Failed to clone repository")
        return "Failed to clone repository"

    # Switch to the initial branch
    checkout_message = git_checkout_branch(repo_path, initial_branch)
    if not checkout_message.startswith("Switched"):
        logging.error("Failed to switch to initial branch: " + checkout_message)
        return "Failed to switch to initial branch: " + checkout_message

    # Create a new branch with a random name and switch to it
    new_branch_name = generate_random_branch_name()
    try:
        repo = Repo(repo_path)
        repo.git.checkout('-b', new_branch_name)
        return new_branch_name, repo_path
    except GitCommandError as e:
        logging.error(e)
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
        logging.error("Failed to add changes: " + add_message)
        return "Failed to add changes: " + add_message

    # Commit changes
    commit_message = git_commit(repo_path, commit_message)
    if not commit_message.startswith("Commit"):
        logging.error("Failed to commit changes: " + commit_message)
        return "Failed to commit changes: " + commit_message

    # Push changes
    current_branch = Repo(repo_path).active_branch.name
    push_message = git_push(repo_path, current_branch)
    if not push_message.startswith("Push"):
        logging.error("Failed to push changes: " + push_message)
        return "Failed to push changes: " + push_message

    return "Add, commit, and push operations were successful"

def open_pull_request(repo_url, source_branch, target_branch):
    logging.info("Opening pull request from {} to {}".format(source_branch, target_branch))
    owner, repo = parse_repo_url(repo_url)

    # Create the URL for the pull request
    pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls"

    # Get the GitHub token from the environment
    github_token = GITHUB
