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
    init.generate_hosts(config["hosts"]["manager"], config["hosts"]["vulnboxes"])

    # Install OpenVPN server on master
    playbook = [{
        "name": "Install the VPN server",
        "hosts": "manager",
        "become": "yes",
        "roles": [{
            "role": "kyl191.openvpn",
            "clients": ["vpn"],
            "openvpn_port": config["vpn"]["port"],
            "openvpn_duplicate_cn": "true",
            "openvpn_server_network": config["vpn"]["network"][:-3], # TODO: get subnet from here
            "openvpn_server_netmask": "255.255.255.0",
            "openvpn_fetch_config_dir": "../../",
            "openvpn_push": [f"route {config['networks'][0]['cidr'][:-3]} 255.255.255.0"] # TODO: select variable subnet mask
        }]
    }]
    with open("ansible/project/vpn.yml", 'w') as f:
        yaml.dump(playbook, f)

    # Execute the vpn installation
    r = ansible_runner.run(
        private_data_dir=settings.PRIVATE_DATA_DIR,
        playbook='vpn.yml'
    )
    print("{}: {}".format(r.status, r.rc))
    print("Final status:")
    print(r.stats)
