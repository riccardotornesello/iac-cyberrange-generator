import sys

from app.parser import parse_config
from app.terraform import (
    save_terraform_file,
    validate_terraform_file,
    apply_terraform_file,
    get_terraform_output,
    destroy_terraform_file,
)
from app.ansible import generate_hosts_file
from app.keys import create_ssh_key_pair

if __name__ == "__main__":
    # Get the action from the first argument (apply, destroy, rebuild) or default to apply
    action = sys.argv[1] if len(sys.argv) > 1 else "apply"
    if action not in ["apply", "destroy", "rebuild"]:
        print("Invalid action. Use apply, destroy or rebuild.")
        sys.exit(1)

    if action == "destroy":
        destroy_terraform_file()
        sys.exit(0)
    elif action == "rebuild":
        destroy_terraform_file()

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

    terraform_out = get_terraform_output()

    """
    CONFIGURATION
    """

    vpn_credentials = {
        "name": "vpn",
        "username": "vpn",
        "password": "soj893f4hIYa!",
        "ip": terraform_out["vpn-public-ip"],
    }

    hosts_credentials = [
        {
            "name": host.name,
            "username": host.username,
            "password": host.password,
            "ip": terraform_out[host.name + "-private-ip"],
        }
        for host in config.hosts
    ]

    create_ssh_key_pair()
    generate_hosts_file(vpn_credentials, hosts_credentials)
