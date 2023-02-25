from typing import Any, Dict
from dotenv import load_dotenv
import os
import json
from fastapi import FastAPI, Request
from handlers import map_handler

from model.config import YadConfig
from model.github import IssueCommentPayload


load_dotenv()

CONFIG = YadConfig.from_file("./yad.toml")

app = FastAPI()


@app.get("/")
async def get_root(request: Request):
    print(await request.body())
    return {"hello": "world"}


@app.post("/api/v1/issue_comment")
async def post_root(request: Request, payload: Dict[str, Any]):
    event_header = request.headers["x-github-event"]
    if event_header is not None:
        handler = map_handler(event_header, payload["action"], payload)
        handler.handle()

    return None
