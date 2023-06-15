# from test_blob import blob
from git_actions import clone_and_create_new_branch,git_add_commit_push,open_pull_request
from gh_bot import notify_pr_commenter_of_proposal
import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")


def add_two_numbers(a, b) -> int:
    return a + b
    
def process_comment(payload):
    ssh_url = payload["pull_request"]["head"]['repo']['ssh_url']
    source_branch_name = payload["pull_request"]["head"]["ref"]
    commented_on_file = payload["comment"]["path"]
    comment_body = payload["comment"]["body"]
    pr_number = payload["pull_request"]["number"]
    comment_id = payload["comment"]["id"]

    new_branch_name, directory = clone_and_create_new_branch(ssh_url, source_branch_name)
    file_to_update = os.path.join(directory, commented_on_file)
    existing_code = read_file(file_to_update)
    new_code = ai_magic(comment_body, existing_code)

    overwrite_file(file_to_update, new_code)
    git_add_commit_push(directory, new_branch_name)
    
    pull_request_message = open_pull_request(ssh_url, new_branch_name, source_branch_name)

    notify_pr_commenter_of_proposal(pr_number, comment_id, pull_request_message)


# write me a function that reads the contents of a file and returns a string
def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()


def ai_magic(comment_body, code_base, **kwargs) -> str:
    prompt = f"The following review comment was made as a suggestion to improve the codebase:" \
             f"\n{comment_body}\n" \
             f"The change should be made in the following file:\n{code_base}\n" \
             f"Please implement the suggested changes in the codebase shown below:\n"

    prompt += code_base

    chat_completion = openai.Completion.create(
        model="text-davinci-002",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        n=1,
        stop=None,
        timeout=60,
    )

    suggestions = chat_completion.choices[0].text

    # get rid of the prompt in the output
    adjusted_code = suggestions.replace(prompt, "")

    print(f"response: {adjusted_code}")
    return adjusted_code


def overwrite_file(file_path, new_file_contents):
    with open(file_path, "w") as f:
        f.write(new_file_contents)