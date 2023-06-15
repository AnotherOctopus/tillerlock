import os
from github import Github, GithubIntegration
import openai

REPO_NAME="tillerlock"
OWNER="AnotherOctopus"
APP_ID = '348063'
openai.api_key = os.getenv("OPENAI_API_KEY")
BOT_PRIV_KEY = os.getenv("BOT_PRIV_KEY")
JIRA_API_KEY = os.getenv("JIRA_API_KEY")

# Create an GitHub integration instance
git_integration = GithubIntegration(
    APP_ID,
    BOT_PRIV_KEY,
)