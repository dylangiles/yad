from typing import Dict, Any
import argparse
import shlex

from .handler import Handler


class IssueCommentHandler(Handler):
    PARSER = argparse.ArgumentParser(prog="PROG")
    PARSER.add_argument("user")

    SUB_PARSERS = PARSER.add_subparsers(dest="subcommand")

    PARSER_APPROVE = SUB_PARSERS.add_parser("approve")

    PARSER_REVIEWER = SUB_PARSERS.add_parser("reviewer")
    PARSER_REVIEWER.add_argument("reviewer_name")

    PARSER_REVIEWER_SHORT = SUB_PARSERS.add_parser("r")
    PARSER_REVIEWER_SHORT.add_argument("reviewer_name")

    PARSER_CLOSE = SUB_PARSERS.add_parser("close")
    PARSER_CLOSE.add_argument("-l", "--lock", dest="lock", action="store_true")

    PARSER_CLOSE_SHORT = SUB_PARSERS.add_parser("c")
    PARSER_CLOSE_SHORT.add_argument("-l", "--lock", dest="lock", action="store_true")

    def __init__(self, action: str, payload: Dict[str, Any]):
        super().__init__(action, payload)

        self.command: str = payload["comment"]["body"]
        self.owner: str = payload["repository"]["owner"]["login"]
        self.repo: str = payload["repository"]["name"]
        self.issue_number: int = payload["issue"]["number"]
        self.pull_request_url: str = (
            payload["issue"]["pull_request"]["url"]
            if payload["issue"]["pull_request"] is not None
            else None
        )

        self.comment_submitter: str = payload["comment"]["user"]["login"]

    def handle(self):
        self.args = self.parse_command()
        if self.args is None:
            return

        if self.args.subcommand in ["approve", "a"]:
            # TODO
            pass

        elif self.args.subcommand in ["reviewer", "r"]:
            if self.args.reviewer_name is None:
                return

            reviewer_name = (
                self.args.reviewer_name[1:]
                if self.args.reviewer_name[0] == "@"
                else self.args.reviewer_name
            )
            self.github_client.assign_user_to_issue(
                self.owner, self.repo, self.issue_number, [reviewer_name]
            )
            self.github_client.comment_on_issue(
                self.owner,
                self.repo,
                self.issue_number,
                f"@{self.comment_submitter} has requested @{reviewer_name} for review of this issue.",
            )

        elif self.args.subcommand in ["close", "c"]:
            if self.pull_request_url is None:
                self.client.comment_on_issue(
                    self.owner,
                    self.repo,
                    self.issue_number,
                    f"Yad failed to process the previous command.",
                )
                return

            pull_request = self.github_client.raw_get(self.pull_request_url)

            self.github_client.close_pull_request(
                self.owner, self.repo, pull_request["number"]
            )
            if self.args.lock:
                self.github_client.lock_conversation(
                    self.owner, self.repo, self.issue_number, "resolved"
                )

    def parse_command(self):
        try:
            return IssueCommentHandler.PARSER.parse_args(shlex.split(self.command))
        except:
            return None
