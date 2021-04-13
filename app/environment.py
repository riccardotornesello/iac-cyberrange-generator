import os

from . import settings


def add_var(key: str, value: str):
    env_file_path = os.path.join(settings.PRIVATE_DATA_DIR, "env/envvars")
    with open(env_file_path, "a") as f:
        f.writelines(f"{key}: {value}\n")
