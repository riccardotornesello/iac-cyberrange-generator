import sys
import yaml
import ansible_runner

from app import environment, init, cloud

if __name__ == "__main__":
    with open("config.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    init.move_old()
    init.create_folders()

    environment.add_extravar("openvpn_port", config["vpn"]["port"])

    provider = cloud.configure_provider(config["cloud"])

    playbook = provider.provision(config["networks"], config["hosts"])
    with open("ansible/project/provisioning.yml", 'w') as f:
        yaml.dump(playbook, f)

    r = ansible_runner.run(private_data_dir="ansible",
                           playbook='provisioning.yml')
    print("{}: {}".format(r.status, r.rc))
    # successful: 0
    for each_host_event in r.events:
        print(each_host_event['event'])
    print("Final status:")
    print(r.stats)
