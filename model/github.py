from datetime import datetime
from pydantic import BaseModel, root_validator
from typing import Any, Dict, List
from requests.auth import HTTPBasicAuth


class GithubAuth:
    def __init__(self, username: str, token: str):
        self.username = username
        self.token = token

    def as_basic_auth(self) -> HTTPBasicAuth:
        return HTTPBasicAuth(username=self.username, password=self.token)


class PayloadBase(BaseModel):
    action: str


class User(BaseModel):
    login: str
    id: int
    node_id: str
    avatar_url: str
    gravatar_id: str
    url: str
    html_url: str
    html_url: str
    followers_url: str
    following_url: str
    gists_url: str
    starred_url: str
    subscriptions_url: str
    organizations_url: str
    repos_url: str
    events_url: str
    received_events_url: str
    type: str
    site_admin: bool


class PullRequest(BaseModel):
    url: str
    html_url: str
    diff_url: str
    patch_url: str
    merged_at: datetime


class Reactions(BaseModel):
    url: str
    total_count: int
    # +1": 0,
    # -1": 0,
    laugh: int
    hooray: int
    confused: int
    heart: int
    rocket: int
    eyes: int


class Issue(BaseModel):
    url: str
    repository_url: str
    labels_url: str
    comments_url: str
    events_url: str
    html_url: str
    id: int
    node_id: str
    number: int
    title: str
    user: User
    labels: List[str]
    state: str
    locked: bool
    assignee: User
    assignees: List[User]
    # milestone": null,
    comments: int
    created_at: datetime
    updated_at: datetime
    # closed_at": null,
    author_association: str
    # "active_lock_reason": null,
    draft: bool
    pull_request: PullRequest
    # "body": null,
    reactions: Reactions
    timeline_url: str
    # "performed_via_github_app": null,
    # "state_reason": null


class IssueCommentPayload(BaseModel):
    action: str
    issue: Issue
    sender: User
    extra: Dict[str, Any]

    @root_validator(pre=True)
    def build_extra(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        all_required_field_names = {
            field.alias for field in cls.__fields__.values() if field.alias != "extra"
        }  # to support alias

        extra: Dict[str, Any] = {}
        for field_name in list(values):
            if field_name not in all_required_field_names:
                extra[field_name] = values.pop(field_name)
        values["extra"] = extra
        return values
