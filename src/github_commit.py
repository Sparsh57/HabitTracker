import requests
from dateutil import parser
from datetime import timedelta
from dotenv import load_dotenv
import os

load_dotenv()


# Replace these variables with your repository details
def get_last_commit_date():
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
    USERNAME = os.getenv("USERNAME")
    REPO_NAME = os.getenv("REPO_NAME")
    BRANCH_NAME = os.getenv("BRANCH_NAME")

    # GitHub API URL for the commits of a specific branch
    url = f"https://api.github.com/repos/{USERNAME}/{REPO_NAME}/commits?sha={BRANCH_NAME}"

    # Headers for authentication
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Make a request to get the list of commits
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        commits = response.json()
        if commits:
            latest_commit = commits[0]
            print(f"Latest commit: {commits[0]['commit']['message']}")
            print(f"Commit SHA: {commits[0]['sha']}")
            print(f"Author: {commits[0]['commit']['author']['name']}")
            print(f"Date: {parser.parse(latest_commit['commit']['author']['date']) + timedelta(hours=5.5)}")
            return (parser.parse(latest_commit['commit']['author']['date']) + timedelta(hours=5.5)).date()
        else:
            return None
            print("No commits found on this branch.")
    else:
        print(f"Failed to retrieve commits: {response.status_code}")
        print(response.json())
        return None


if __name__ == '__main__':
    print(get_last_commit_date())
