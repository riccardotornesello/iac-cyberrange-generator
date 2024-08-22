import sys

from app.parser import parse_config
from app.provisioning import (
    save_terraform_file,
    validate_terraform_file,
    apply_terraform_file,
)

if __name__ == "__main__":
    """
    INITIALIZAZION
    """

    # Open the config file
    # TODO: allow custom file name
    try:
        config = parse_config("config.yml")
    except Exception as e:
        print(e)
        sys.exit(1)

    """
    PROVISIONING
    """

    save_terraform_file(config)
    validate_terraform_file()
    apply_terraform_file()
