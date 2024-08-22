import subprocess
import sys
import os

from .classes import Config
from .terraform.providers import TerraformAzure


PATH = ".generated/terraform"


def save_terraform_file(config: Config):
    terraform = TerraformAzure()
    content = terraform.provision(config)

    file_path = f"{PATH}/main.tf"

    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    with open(file_path, "w") as f:
        f.write(content)

    try:
        subprocess.run(["terraform", f"-chdir={PATH}", "init"], check=True)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)

    return file_path


def validate_terraform_file():
    try:
        subprocess.run(["terraform", f"-chdir={PATH}", "validate"], check=True)
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)


def apply_terraform_file():
    try:
        subprocess.run(
            ["terraform", f"-chdir={PATH}", "apply", "-auto-approve"], check=True
        )
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)


def get_terraform_output(var):
    try:
        output = subprocess.run(
            ["terraform", f"-chdir={PATH}", "output", var],
            capture_output=True,
            text=True,
        )
        return output.stdout.strip().replace('"', "")
    except subprocess.CalledProcessError as e:
        print(e)
        sys.exit(1)
