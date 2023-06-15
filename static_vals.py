import os
from github import Github, GithubIntegration

REPO_NAME="tillerlock"
OWNER="AnotherOctopus"
BOT_PRIV_KEY="tillerlock-bot.2023-06-15.private-key.pem"
APP_ID = '348063'

with open(
        os.path.normpath(os.path.expanduser(BOT_PRIV_KEY)),
        'r'
) as cert_file:
    app_key = cert_file.read()

# Create an GitHub integration instance
git_integration = GithubIntegration(
    APP_ID,
    app_key,
)