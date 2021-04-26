import sys
import yaml
import ansible_runner

from app import environment, init, cloud, settings

if __name__ == "__main__":
    """
    INITIALIZAZION
    """

    # Open the config file
    with open("config.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    # Clean and create the needed directories
    init.move_old()
    init.create_folders()

    # Create the rsa keys
    init.generate_keys()

    """
    PROVISIONING
    """

    # Configure openvpn variables for ansible
    environment.add_extravar("openvpn_port", config["vpn"]["port"])

    # Create a cloud instance
    provider = cloud.configure_provider(config["cloud"])

    # Ask the cloud instance to create a provisioning playbook and save that
    playbook = provider.provision(config["networks"], config["hosts"])
    with open("ansible/project/provisioning.yml", 'w') as f:
        yaml.dump(playbook, f)

    # Execute the provisioning
    r = ansible_runner.run(
        private_data_dir=settings.PRIVATE_DATA_DIR,
        playbook='provisioning.yml'
    )
    print("{}: {}".format(r.status, r.rc))
    print("Final status:")
    print(r.stats)

    # Generate hosts inventory
    init.generate_hosts(config["hosts"]["manager"],
                        config["hosts"]["vulnboxes"])

    # Install OpenVPN server on master
    playbook = [{
        "name": "Install the VPN server",
        "hosts": "manager",
        "become": "yes",
        "roles": [{
            "role": "kyl191.openvpn",
            "clients": ["vpn"],
            "openvpn_port": config["vpn"]["port"],
            "openvpn_duplicate_cn": True,
            # TODO: get subnet from here
            "openvpn_server_network": config["vpn"]["network"][:-3],
            "openvpn_server_netmask": "255.255.255.0",
            "openvpn_fetch_config_dir": "../../",
            # TODO: select variable subnet mask
            "openvpn_push": [f"route {config['networks'][0]['cidr'][:-3]} 255.255.255.0"],
            "openvpn_client_register_dns": False,
            "openvpn_redirect_gateway": False
        }]
    }]
    with open("ansible/project/vpn.yml", 'w') as f:
        yaml.dump(playbook, f)

    r = ansible_runner.run(
        private_data_dir=settings.PRIVATE_DATA_DIR,
        playbook='vpn.yml'
    )
    print("{}: {}".format(r.status, r.rc))
    print("Final status:")
    print(r.stats)

    # Config vulnbox services
    for vulnbox in config["hosts"]["vulnboxes"]:
        roles = []

        for service in vulnbox["services"]:
            roles.append({
                "role": service["type"],
                **service["options"]
            })

        playbook = [{
            "name": f"Config {vulnbox['hostname']}",
            "hosts": vulnbox['hostname'],
            "become": "yes",
            "roles": roles
        }]

        with open(f"ansible/project/config-{vulnbox['hostname']}.yml", 'w') as f:
            yaml.dump(playbook, f)

        r = ansible_runner.run(
            private_data_dir=settings.PRIVATE_DATA_DIR,
            playbook=f"config-{vulnbox['hostname']}.yml"
        )
        print("{}: {}".format(r.status, r.rc))
        print("Final status:")
        print(r.stats)

    # Configure manager
    manager = config["hosts"]["manager"]
    roles = []
    for service in manager["attacks"]:
        roles.append({
            "role": service["type"],
            **service["options"]
        })

    playbook = [{
        "name": f"Config {manager['hostname']}",
        "hosts": "manager",
        "become": "yes",
        "roles": roles
    }]

    with open(f"ansible/project/config-{manager['hostname']}.yml", 'w') as f:
        yaml.dump(playbook, f)

    r = ansible_runner.run(
        private_data_dir=settings.PRIVATE_DATA_DIR,
        playbook=f"config-{manager['hostname']}.yml"
    )
    print("{}: {}".format(r.status, r.rc))
    print("Final status:")
    print(r.stats)
