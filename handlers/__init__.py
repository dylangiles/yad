from typing import Dict, Any

from handlers.issue_comment import IssueCommentHandler


HANDLER_MAP = {"issue_comment": IssueCommentHandler}


def map_handler(event: str, action: str, payload: Dict[str, Any]):
    if event in HANDLER_MAP:
        return HANDLER_MAP[event](action, payload)
