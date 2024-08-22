import yaml
import os


PATH = ".generated/ansible"


def generate_hosts_file(vpn_credentials, hosts_credentials):
    data = {
        "vpn-group": {
            "hosts": {
                vpn_credentials["name"]: {
                    "ansible_host": vpn_credentials["ip"],
                    "ansible_user": vpn_credentials["username"],
                    "ansible_password": vpn_credentials["password"],
                }
            }
        },
        "hosts-group": {
            "hosts": {
                host["name"]: {
                    "ansible_host": host["ip"],
                    "ansible_user": host["username"],
                    "ansible_password": host["password"],
                }
                for host in hosts_credentials
            },
            "vars": {
                "ansible_ssh_common_args": f'-o ProxyCommand="ssh -p 22 -W %h:%p -q {vpn_credentials["username"]}@{vpn_credentials["ip"]} -i ./.generated/keys/id_rsa"',
            },
        },
    }

    os.makedirs(PATH, exist_ok=True)

    with open(f"{PATH}/hosts.yml", "w") as f:
        yaml.dump(data, f)
