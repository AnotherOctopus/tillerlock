
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

    branch_name, directory = clone_and_create_new_branch(repo_name, branch_name)
    file_to_update = os.path.join(directory, commented_on_file)

    print(file_to_update)
    existing_code =read_file(file_to_update)
    new_code = ai_magic(comment_body, existing_code)

    overwrite_file(file_to_update, new_code)
    git_add_commit_push(directory, branch_name)

    notify_pr_commenter_of_proposal(pr_number, comment_id, branch_name)

    
def ai_magic(comment_body, full_codebase_to_modify) -> str:
    return """
    def foo():
        return 1
    """

#write me a function that reads the contexts of a file and returns a string
def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def overwrite_file(file_path, new_file_contents):
    with open(file_path, "w") as f:
        f.write(new_file_contents)