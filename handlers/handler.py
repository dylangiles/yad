import os
from typing import Dict, Any
from core.github import GithubClient


class Handler:
    def __init__(self, action: str, payload: Dict[str, Any]):
        self.action = action
        self.action_user = os.getenv("ACTION_USER")
        self.payload = payload
        self.github_client = GithubClient(
            self.action_user, os.getenv("GITHUB_ACCESS_TOKEN")
        )
