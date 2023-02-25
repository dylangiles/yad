from model.github import PayloadBase, GithubAuth
from handlers.github import GithubClient
import os
import argparse
import shlex


def issue_comment_handler(**kwargs):
    if kwargs["action"] == "created":
        command: str = kwargs["comment"]["body"]
        print("Received command: %s" % command)
        action_user = os.getenv("ACTION_USER")

        parser = argparse.ArgumentParser(prog="PROG")
        parser.add_argument("user")

        sub_parsers = parser.add_subparsers(dest="subcommand")

        parser_approve = sub_parsers.add_parser("approve")

        parser_reviewer = sub_parsers.add_parser("reviewer")
        parser_reviewer.add_argument("reviewer_name")

        parser_reviewer_short = sub_parsers.add_parser("r")
        parser_reviewer_short.add_argument("reviewer_name")

        parser_close = sub_parsers.add_parser("close")
        parser_close.add_argument("-l", "--lock", dest="lock", action="store_true")

        parser_close_short = sub_parsers.add_parser("c")
        parser_close_short.add_argument(
            "-l", "--lock", dest="lock", action="store_true"
        )

        try:
            args = parser.parse_args(shlex.split(command))
        except:
            return

        if args.user[0 : len(action_user) + 1] != "@%s" % action_user:
            return

        # if args.subcommand not in ["approve", "a", "reviewer", "r"]:
        #     return

        repo_owner = kwargs["repository"]["owner"]["login"]
        repo = kwargs["repository"]["name"]
        issue_number = kwargs["issue"]["number"]
        pull_request_url = (
            kwargs["issue"]["pull_request"]["url"]
            if kwargs["issue"]["pull_request"] is not None
            else None
        )

        comment_submitter = kwargs["comment"]["user"]["login"]
        client = GithubClient(action_user, os.getenv("GITHUB_ACCESS_TOKEN"))
        if args.subcommand == "approve":
            client.comment_on_issue(
                repo_owner,
                repo,
                issue_number,
                "Approved by @%s" % approved_by,
            )

        elif args.subcommand == "reviewer" or args.subcommand == "r":
            if args.reviewer_name is None:
                return

            reviewer_name = (
                args.reviewer_name[1:]
                if args.reviewer_name[0] == "@"
                else args.reviewer_name
            )
            client.assign_user_to_issue(repo_owner, repo, issue_number, [reviewer_name])
            client.comment_on_issue(
                repo_owner,
                repo,
                issue_number,
                f"@{comment_submitter} has requested @{reviewer_name} for review of this issue.",
            )

        elif args.subcommand == "close" or args.subcommand == "c":
            if pull_request_url is None:
                client.comment_on_issue(
                    repo_owner,
                    repo,
                    issue_number,
                    f"Yad failed to process the previous command.",
                )
                return

            pull_request = client.raw_get(pull_request_url)

            client.close_pull_request(repo_owner, repo, pull_request["number"])
            if args.lock:
                client.lock_conversation(repo_owner, repo, issue_number, "resolved")


HANDLER_MAP = {"issue_comment": issue_comment_handler}


def map_handler(event: str, **kwargs):
    if event in HANDLER_MAP:
        HANDLER_MAP[event](**kwargs)
