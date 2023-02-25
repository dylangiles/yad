from dotenv import load_dotenv
import os
from github import Github

from model.config import YadConfig


load_dotenv()

g = Github(os.getenv("GITHUB_ACCESS_TOKEN"))

CONFIG = YadConfig.from_file("./yad.toml")
print(CONFIG.target_repos)
repos = [g.get_user().get_repos(repo)[0] for repo in CONFIG.target_repos]
print(repos)
