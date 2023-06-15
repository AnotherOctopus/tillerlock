import os
from github import Github, GithubIntegration

REPO_NAME="tillerlock"
OWNER="AnotherOctopus"
APP_ID = '348063'

with open(
        os.path.normpath(os.path.expanduser('tillerlock-bot.2023-06-15.private-key.pem')),
        'r'
) as cert_file:
    app_key = cert_file.read()

# Create an GitHub integration instance
git_integration = GithubIntegration(
    APP_ID,
    app_key,
)