from typing import List
import toml


class IssueCommentConfig:
    message_override: str

    def __init__(self, **kwargs):
        self.message_override = (
            kwargs["message_override"] if "message_override" in kwargs else None
        )


class HandlersConfig:
    issue_comment: IssueCommentConfig

    def __init__(self, **kwargs):
        self.issue_comment = (
            kwargs["issue_comment"] if "issue_comment" in kwargs else None
        )


class YadConfig:
    target_repos: List[str]
    handlers: HandlersConfig

    def __init__(self, **kwargs):
        self.target_repos = kwargs["target_repos"] if "target_repos" in kwargs else None
        self.handlers = (
            HandlersConfig(kwargs["handlers"]) if "handlers" in kwargs else None
        )

    def from_file(file_name: str):
        with open(file_name, "r") as f:
            toml_string = f.read()

        toml_data = toml.loads(toml_string)
        return YadConfig(**toml_data)
