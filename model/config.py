from typing import List
import toml


class YadConfig:
    target_repos: List[str]

    def __init__(self, **kwargs):
        self.target_repos = kwargs["target_repos"] if "target_repos" in kwargs else None

    def from_file(file_name: str):
        with open(file_name, "r") as f:
            toml_string = f.read()

        toml_data = toml.loads(toml_string)
        return YadConfig(**toml_data)
