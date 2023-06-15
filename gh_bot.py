
from github import Github, GithubIntegration
from static_vals import git_integration, REPO_NAME, OWNER
import logging

def notify_pr_commenter_of_proposal(pr_number: int, comment_id: int, proposal_branch):
    response = "That was a great comment. Can I just say, you're such a perceptive and attentive person, for taking the time to not only go through this code but also reccomend ways it could be improved. With my immense robo-brain, I took a swag at fixing the issue you pointed out, and you can see my changes [here](https://github.com/AnotherOctopus/tillerlock/tree/{proposal_branch}). Feel free to merge it in!".format(proposal_branch=proposal_branch)
    respond_to_pr_comment(pr_number, comment_id, response)  

def respond_to_pr_comment(pr_number: int, comment_id: int, body: str):
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
    comment = repo.get_pull(pr_number).create_review_comment_reply(comment_id,body)
    logging.info(f"Created comment {comment.id} on PR {pr_number}")
