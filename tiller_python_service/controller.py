def multiply_two_numbers(a, b) -> int:
    return a * b

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
    new_code = existing_code.replace("add_two_numbers(a, b) -> int:", "multiply_two_numbers(a, b) -> int:")

    overwrite_file(file_to_update, new_code)
    git_add_commit_push(directory, new_branch_name)
    
    pull_request_message = open_pull_request(ssh_url, new_branch_name, source_branch_name)

    notify_pr_commenter_of_proposal(pr_number, comment_id, pull_request_message)


#write me a function that reads the contents of a file and returns a string
def read_file(file_path):
    with open(file_path, "r") as f:
        return f.read()

def ai_magic(comment_body, full_codebase_to_modify, **kwargs) -> str:
    prompt = _construct_prompt(comment_body, full_codebase_to_modify, kwargs=kwargs)

    chat_completion = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        temperature=0.5,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    response = chat_completion.choices[0].text
    print(f"response: {response}")
    return response


def overwrite_file(file_path, new_file_contents):
    with open(file_path, "w") as f:
        f.write(new_file_contents)

def _construct_prompt(comment_body, code_base, **kwargs):
    prompt = f"Given the following review comment that was made as a suggestion to improve the codebase," \
             f"please do your best to fix the codebase to adhere to the suggestions of the review comment." \
             f"The comment is listed as such: \n{comment_body}\n, and the change should be made in the file below: " \
             f"\n{code_base}\n. Your response should only include the entirety of the adjusted codebase, and no other " \
             f"text.\n"

    prompt += "You: "

    return prompt