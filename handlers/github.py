from typing import Any, Dict, List, Union
from model.github import GithubAuth

import requests
from requests.auth import HTTPBasicAuth
import json


class GithubClient:
    ROOT_URL = "https://api.github.com"

    def __init__(self, username: str, token: str):
        self.username = username
        self.token = token

    def _get_auth(self) -> HTTPBasicAuth:
        return GithubAuth(self.username, self.token).as_basic_auth()

    def raw_get(
        self, url: str, data: Union[Dict[str, Any], None] = None
    ) -> Dict[str, Any]:
        return requests.get(
            url, headers=self.get_default_headers(), json=data, auth=self._get_auth()
        ).json()

    def patch(self, resource: str, json: Dict[str, Any]):
        requests.patch(
            GithubClient.get_url(resource),
            headers=self.get_default_headers(),
            json=json,
            auth=self._get_auth(),
        )

    def put(self, resource: str, json: Dict[str, Any]):
        requests.put(
            GithubClient.get_url(resource),
            headers=self.get_default_headers(),
            json=json,
            auth=self._get_auth(),
        )

    def comment_on_issue(
        self, repo_owner: str, repo: str, issue_number: int, comment_body: str
    ):
        resource = "/repos/%s/%s/issues/%d/comments" % (repo_owner, repo, issue_number)
        result = requests.post(
            GithubClient.get_url(resource),
            headers=self.get_default_headers(),
            json=dict(body=comment_body),
            auth=self._get_auth(),
        )

    def review_pull_request(
        self, repo_owner: str, repo: str, pull_number: int, event: str
    ):
        if event not in ["APPROVE", "REQUEST_CHANGES", "COMMENT"]:
            raise ValueError("event must be one of APPROVE, REQUEST_CHANGES, COMMENT")

        resource = f"/repos/{repo_owner}/{repo}/pulls/{pull_number}/reviews"
        result = requests.post(
            GithubClient.get_url(resource),
            headers=self.get_default_headers(),
            json=dict(event=event),
            auth=self._get_auth(),
        )

    def assign_user_to_issue(
        self, owner: str, repo: str, issue_number: int, assignees: List[str]
    ):
        resource = f"/repos/{owner}/{repo}/issues/{issue_number}/assignees"
        requests.post(
            GithubClient.get_url(resource),
            headers=self.get_default_headers(),
            json=dict(assignees=assignees),
            auth=self._get_auth(),
        )

    def close_pull_request(self, owner: str, repo: str, pull_number: int):
        resource = f"/repos/{owner}/{repo}/pulls/{pull_number}"
        self.patch(resource, dict(state="closed"))

    def lock_conversation(self, owner: str, repo: str, issue_number: int, reason: str):
        if reason not in ["off-topic", "too heated", "resolved", "spam"]:
            raise ValueError(
                "Lock reason must be one of: off-topic, too heated, resolved, spam"
            )

        resource = f"/repos/{owner}/{repo}/issues/{issue_number}/lock"
        self.put(resource, dict(lock_reason=reason))

    @staticmethod
    def get_url(resource: str) -> str:
        return GithubClient.ROOT_URL + resource

    @staticmethod
    def get_default_headers() -> Dict[str, str]:
        return {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
