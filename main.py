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
    for each_host_event in r.events:
        print(each_host_event['event'])
    print("Final status:")
    print(r.stats)
