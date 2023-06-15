# from test_blob import blob
from git_actions import clone_and_create_new_branch,git_add_commit_push,open_pull_request
from git_actions import clone_and_create_new_branch, git_add_commit_push
from gh_bot import notify_pr_commenter_of_proposal
import logging
import os
import openai

LOGGER = logging.getLogger(__name__)

def multiply_these_numbers(a, b):
    return a * b

def should_generate_fix(payload):
    comment_body = payload["comment"]["body"]
    if "help tiller" in comment_body.lower():
        return True
    return False


def process_comment(payload):
    if not should_generate_fix(payload):
        return
    ssh_url = payload["pull_request"]["head"]['repo']['ssh_url']
    clone_url = payload["pull_request"]["head"]['repo']['clone_url']
    source_branch_name = payload["pull_request"]["head"]["ref"]
    commented_on_file = payload["comment"]["path"]
    comment_body = payload["comment"]["body"]
    pr_number = payload["pull_request"]["number"]
    comment_id = payload["comment"]["id"]

    print(clone_url, source_branch_name)

    new_branch_name, directory = clone_and_create_new_branch(clone_url, source_branch_name)
    file_to_update = os.path.join(directory, commented_on_file)

    print(file_to_update)
    existing_code =read_file(file_to_update)
    new_code = ai_magic(comment_body, existing_code)

    overwrite_file(file_to_update, new_code)
    git_add_commit_push(directory, new_branch_name)

    pull_request_message = open_pull_request(ssh_url, new_branch_name, source_branch_name)

    notify_pr_commenter_of_proposal(pr_number, comment_id, pull_request_message)


# write me a function that reads the contexts of a file and returns a string
def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()


def ai_magic(comment_body, full_codebase_to_modify, **kwargs) -> str:
    prompt = _construct_prompt(comment_body, full_codebase_to_modify, kwargs=kwargs)

    chat_completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    response = chat_completion.choices[0].message.content
    print(f"response: {response}")
    return response


def overwrite_file(file_path, new_file_contents):
    with open(file_path, "w") as f:
        f.write(new_file_contents)

def _construct_prompt(comment_body, code_base, **kwargs):
    # line_number = kwargs.get("line_number")
    prompt = f"Given the following review comment that was made as a suggestion to improve the codebase, " \
             f"please do your best to fix the codebase to adhere to the suggestions of the review comment." \
             f" The comment is listed as such: \n{comment_body}\n and the change should be made in the file below: " \
             f"`\n{code_base}\n` Your response should only include the entirety of the original codebase with replacements" \
             f" for the recommended adjustments, and no other text, generated commentary, or unnecessary punctuation. " \
             f"This should continue to be valid Python code, and should not add unnecessary newlines.\n" \
             f"Be sure to scan the surrounding context in order to make a thorough and reasonable change to the codebase." \
             f" For example, a recommended change to functionality may entail a change to the function signature. \n"

    prompt += "You: "

    return prompt
