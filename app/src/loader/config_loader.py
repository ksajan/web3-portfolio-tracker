import json
import os


class ConfigLoader:
    def __init__(self, config_file_path: str):
        self.config_file_path = config_file_path

    def load_config(self) -> dict:
        with open(self.config_file_path, "r") as file:
            return json.load(file)

    def set_env_vars(self, config: dict) -> None:
        for key, value in config.items():
            os.environ[key] = value
