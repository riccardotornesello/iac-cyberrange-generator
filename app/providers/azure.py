from .. import environment


class Azure():
    def __init__(self, options: dict):
        for k, v in options.items():
            environment.add_var(k, v)

    def provision(self, networks: list, hosts: dict):
        with open("keys/public.key", "r") as f:
            public_key = f.readline().strip()

        # TODO: make variable
        environment.add_extravar("azure_resourcegroup_name", "cyberrange")
        # TODO: make variable
        environment.add_extravar("azure_resourcegroup_location", "westeurope")
        # TODO: make variable
        environment.add_extravar("azure_security_group_name", "myNetworkSecurityGroup")
        # TODO: make variable
        environment.add_extravar("azure_publicip_name", "myPublicIP")

        # TODO: parse multiple networks
        network = networks[0]
        environment.add_extravar("azure_vnet_name", network["name"])
        environment.add_extravar("azure_vnet_cidr", network["cidr"])
        environment.add_extravar("subnet_name", network["name"])
        environment.add_extravar("subnet_cidr", network["cidr"])

        roles = []
        roles.append({
            "role": "azure-init"
        })
        roles.append({
            "role": "azure-network"
        })
        roles.append({
            "role": "azure-vm-main",
            "vm_name": hosts["manager"]["hostname"],
            "azure_vm_size": "Standard_B1s",  # TODO: make variable
            "vm_username": hosts["manager"]["username"],
            "vm_password": hosts["manager"]["password"],
            "vm_private_ip": hosts["manager"]["ip"],
            "vm_public_key": public_key
        })

        for vulnbox in hosts["vulnboxes"]:
            roles.append({
                "role": "azure-vm",
                "vm_name": vulnbox["hostname"],
                "azure_vm_size": "Standard_B1s",  # TODO: make variable
                "vm_username": vulnbox["username"],
                "vm_password": vulnbox["password"],
                "vm_private_ip": vulnbox["ip"],
            })

        return [{
            "name": "Provisioning",
            "hosts": "localhost",
            "roles": roles
        }]
