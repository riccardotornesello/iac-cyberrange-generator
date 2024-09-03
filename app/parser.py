"""
YAML parser.
Reads and checks the configuration file, then returns the configuration in standard format.
"""

import yaml

from .classes import Project, Network, Host, Subnet, Config, Vpn, Service


def parse_config(config_file):
    with open(config_file, "r") as f:
        yaml_config = yaml.safe_load(f)

    # TODO: Add configuration checks

    project = Project(
        name=yaml_config["project"]["name"],
        location=yaml_config["project"]["location"],
    )
    network = Network(
        cidr=yaml_config["network"]["cidr"],
    )
    subnets = [
        Subnet(
            name=subnet["name"],
            cidr=subnet["cidr"],
        )
        for subnet in yaml_config["network"]["subnets"]
    ]
    hosts = [
        Host(
            name=host["name"],
            username=host["username"],
            password=host["password"],
            ip=host["ip"],
            subnet=host["subnet"],
            services=[
                Service(name=service["name"]) for service in host.get("services", [])
            ],
        )
        for host in yaml_config["hosts"]
    ]
    vpn = Vpn(
        subnet=yaml_config["vpn"]["subnet"],
        lan_ip=yaml_config["vpn"]["lan_ip"],
        vpn_subnet=yaml_config["vpn"]["vpn_subnet"],
    )

    return Config(
        project=project,
        network=network,
        subnets=subnets,
        hosts=hosts,
        vpn=vpn,
    )
