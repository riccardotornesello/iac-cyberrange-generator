import yaml
import os
import socket
import struct
import shutil

import ansible_runner

from app.classes import Host


PATH = ".generated/ansible"

current_path = os.getcwd()


def generate_ansible_inventory(vpn_credentials, hosts_credentials):
    data = {
        "vpn_group": {
            "hosts": {
                vpn_credentials["name"]: {
                    "ansible_host": vpn_credentials["ip"],
                    "ansible_user": vpn_credentials["username"],
                    "ansible_password": vpn_credentials["password"],
                }
            }
        },
        "hosts_group": {
            "hosts": {
                host["name"]: {
                    "ansible_host": host["ip"],
                    "ansible_user": host["username"],
                    "ansible_password": host["password"],
                }
                for host in hosts_credentials
            },
            "vars": {
                "ansible_ssh_common_args": f'-o ProxyCommand="ssh -p 22 -W %h:%p -q {vpn_credentials["username"]}@{vpn_credentials["ip"]} -i {current_path}/.generated/keys/id_rsa"',
            },
        },
    }

    os.makedirs(f"{PATH}/inventory", exist_ok=True)

    with open(f"{PATH}/inventory/hosts.yml", "w") as f:
        yaml.dump(data, f)


def clean_ansible_playbooks():
    shutil.rmtree(f"{PATH}/project", ignore_errors=True)


def generate_vpn_playbook(vpn_subnet):
    network, net_bits = vpn_subnet.split("/")
    host_bits = 32 - int(net_bits)
    netmask = socket.inet_ntoa(struct.pack("!I", (1 << 32) - (1 << host_bits)))

    data = [
        {
            "name": "VPN host configuration",
            "hosts": "vpn_group",
            "become": "yes",
            "roles": [{"role": "openvpn_server"}],
            "vars": {"vpn_subnet_ip": network, "vpn_subnet_mask": netmask},
        }
    ]

    os.makedirs(f"{PATH}/project", exist_ok=True)

    with open(f"{PATH}/project/vpn.yml", "w") as f:
        yaml.dump(data, f)


def generate_host_playbooks(hosts: list[Host]):
    new_playbooks = []

    for host in hosts:
        if len(host.services) > 0:
            new_playbooks.append(host.name)

            data = [
                {
                    "name": f"{host.name} host configuration",
                    "hosts": host.name,
                    "become": "yes",
                    "roles": [{"role": service.name} for service in host.services],
                }
            ]

            os.makedirs(f"{PATH}/project", exist_ok=True)

            with open(f"{PATH}/project/{host.name}.yml", "w") as f:
                yaml.dump(data, f)

    return new_playbooks


def run_playbook(playbook):
    ansible_runner.run(
        private_data_dir=PATH,
        playbook=f"{playbook}.yml",
        roles_path=f"{current_path}/ansible/roles",
    )
