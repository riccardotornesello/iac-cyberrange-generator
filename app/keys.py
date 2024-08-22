import os
import subprocess
import sys


PATH = ".generated/keys"


def create_ssh_key_pair():
    os.makedirs(PATH, exist_ok=True)

    if not os.path.exists(f"{PATH}/id_rsa"):
        try:
            subprocess.run(
                [
                    "ssh-keygen",
                    "-t",
                    "rsa",
                    "-b",
                    "4096",
                    "-C",
                    "ansible",
                    "-f",
                    f"{PATH}/id_rsa",
                    "-N",
                    "",
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            print(e)
            sys.exit(1)
