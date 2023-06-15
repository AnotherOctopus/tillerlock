
from github import Github, GithubIntegration
from static_vals import git_integration, REPO_NAME, OWNER

def respond_to_pr_comment(pr_number: int, comment_id: str, body: str):
    owner = OWNER 
    repo_name = REPO_NAME 

    # Get a git connection as our bot
    # Here is where we are getting the permission to talk as our bot and not
    # as a Python webservice
    git_connection = Github(
        login_or_token=git_integration.get_access_token(
            git_integration.get_repo_installation(owner, repo_name).id
        ).token
    )
    repo = git_connection.get_repo(f"{owner}/{repo_name}")
    print(repo.get_pull(pr_number).comments)
