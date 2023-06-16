# from test_blob import blob
from git_actions import (
    clone_and_create_new_branch,
    git_add_commit_push,
    open_pull_request,
)
from gh_bot import notify_pr_commenter_of_proposal
import logging
import os
import openai
import ast

LOGGER = logging.getLogger(__name__)

def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr)//2
        L = arr[:mid]
        R = arr[mid:]
 
        merge_sort(L)
        merge_sort(R)
 
        i = j = k = 0
 
        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1
 
        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1
 
        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1

def is_valid_python(code):
    try:
        ast.parse(code)
    except SyntaxError:
        return False
    return True


def should_generate_fix(payload):
    comment_body = payload["comment"]["body"]
    if "help tiller" in comment_body.lower():
        return True
    return False


def process_comment(payload):
    if not should_generate_fix(payload):
        return

    ssh_url = payload["pull_request"]["head"]["repo"]["ssh_url"]
    clone_url = payload["pull_request"]["head"]["repo"]["clone_url"]
    source_branch_name = payload["pull_request"]["head"]["ref"]
    commented_on_file = payload["comment"]["path"]
    comment_body = payload["comment"]["body"]
    pr_number = payload["pull_request"]["number"]
    comment_id = payload["comment"]["id"]
    comment_line = payload.get("comment").get("line")

    print(clone_url, source_branch_name)

    new_branch_name, directory = clone_and_create_new_branch(
        clone_url, source_branch_name
    )
    file_to_update = os.path.join(directory, commented_on_file)

    print(file_to_update)
    existing_code = read_file(file_to_update)
    new_code = ai_magic(comment_body, existing_code, line_number=comment_line)

    overwrite_file(file_to_update, new_code)
    git_add_commit_push(directory, new_branch_name)

    pull_request_message = open_pull_request(
        ssh_url, new_branch_name, source_branch_name
    )

    notify_pr_commenter_of_proposal(pr_number, comment_id, pull_request_message)


def add_these_numbers(num1, num2):
    return num1 + num2


# write me a function that reads the contexts of a file and returns a string
def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()


def ai_magic(comment_body, full_codebase_to_modify, **kwargs) -> str:
    print("starting ai magic......")
    prompt = _construct_prompt(comment_body, full_codebase_to_modify, kwargs=kwargs)

    while True:
        print("querying chatgpt for responses")
        chat_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.3,
            n=5,
        )
        print(chat_completion)
        for response in chat_completion.choices:
            msg = response.message.content.replace("", "")
            if is_valid_python(msg):
                response = msg
                print(f"response: {msg}")
                return msg
        print("none of the responses were valid python, retrying...")


def overwrite_file(file_path, new_file_contents):
    with open(file_path, "w") as f:
        f.write(new_file_contents)


def _construct_prompt(comment_body, code_base, **kwargs):
    line_number = kwargs.get("line_number")
    line_number_prompt = "" if not line_number else f" around line {str(line_number)}"
    prompt = (
        f"Given the following review comment that was made as a suggestion to improve the codebase, "
        f"please do your best to fix the codebase to adhere to the suggestions of the review comment."
        f" The comment is listed as such: \n{comment_body}\n and the change should be made in the file below, "
        f"{line_number_prompt}: "
        f"`\n{code_base}\n` Your response should only include the entirety of the original codebase with replacements"
        f" for the recommended adjustments - no other text, generated commentary, or unnecessary punctuation should be present. "
        f"This should continue to be valid Python code, and should not add unnecessary newlines.\n"
        f"Be sure to scan the surrounding context in order to make a thorough and reasonable change to the codebase."
        f"Do not include the comment at the top of the return message." \
        f" For example, a recommended change to functionality may entail a change to the function signature. \n"
    )

    prompt += "You: "

    return prompt