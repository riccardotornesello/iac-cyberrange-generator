import yaml
import os
import socket
import struct

import ansible_runner


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


def generate_vpn_playbook(vpn_subnet):
    network, net_bits = vpn_subnet.split("/")
    host_bits = 32 - int(net_bits)
    netmask = socket.inet_ntoa(struct.pack("!I", (1 << 32) - (1 << host_bits)))

    data = [
        {
            "name": "VPN host configuration",
            "hosts": "vpn-group",
            "become": "yes",
            "roles": [{"role": "openvpn-server"}],
            "vars": {"vpn_subnet_ip": network, "vpn_subnet_mask": netmask},
        }
    ]

    os.makedirs(f"{PATH}/playbooks", exist_ok=True)

    with open(f"{PATH}/playbooks/vpn.yml", "w") as f:
        yaml.dump(data, f)


def run_playbook(playbook):
    ansible_runner.run(
        private_data_dir=".",
        playbook=f"{PATH}/playbooks/{playbook}.yml",
        inventory=f"{PATH}/hosts.yml",
        roles_path="ansible/roles",
    )
