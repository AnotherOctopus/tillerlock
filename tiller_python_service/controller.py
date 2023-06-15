
from test_blob import blob
from git_actions import clone_and_create_new_branch,git_add_commit_push
from gh_bot import notify_pr_commenter_of_proposal
import os

def process_comment(payload):
    repo_name = payload["pull_request"]["head"]['repo']['ssh_url']
    branch_name = payload["pull_request"]["head"]["ref"]
    commented_on_file = payload["comment"]["path"]
    comment_body = payload["comment"]["body"]
    pr_number = payload["pull_request"]["number"]
    comment_id = payload["comment"]["id"]
    pr_title = payload["pull_request"]["title"]

    ticket_name = regex_out_ticket_name(pr_title)
    jira_ticket_body = get_jira_ticket_body(ticket_name)

    branch_name, directory = clone_and_create_new_branch(repo_name, branch_name)
    file_to_update = os.path.join(directory, commented_on_file)

    existing_code = os.open( file_to_update, "r").read()
    new_code = ai_magic(comment_body, existing_code, jira_ticket_body)

    overwrite_file(file_to_update, new_code)
    git_add_commit_push(directory, branch_name)

    notify_pr_commenter_of_proposal(pr_number, comment_id, branch_name)

    
def regex_out_ticket_name(pr_title) -> str:
    pass
def get_jira_ticket_body(ticket_name) -> str:
    pass

def ai_magic(comment_body, full_codebase_to_modify, jira_ticket_body) -> str:
   full_codebase_to_modify 

def overwrite_file(file_path, new_file_contents):
    with open(file_path, "w") as f:
        f.write(new_file_contents)