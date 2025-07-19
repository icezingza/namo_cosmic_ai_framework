# inter_ai_comms/github_mcp_adapter.py

import os
import requests

class GitHubMCPAdapter:
    def __init__(self):
        self.token = os.getenv("GITHUB_TOKEN")
        self.repo = "kanin/namo_cosmic_ai_framework"
        self.api_url = "https://api.github.com"

    def get_commits(self):
        url = f"{self.api_url}/repos/{self.repo}/commits"
        headers = {"Authorization": f"token {self.token}"}
        response = requests.get(url, headers=headers)
        return [commit['commit']['message'] for commit in response.json()]

    def create_issue(self, title, body):
        url = f"{self.api_url}/repos/{self.repo}/issues"
        headers = {"Authorization": f"token {self.token}"}
        payload = {"title": title, "body": body}
        response = requests.post(url, headers=headers, json=payload)
        return response.json()
