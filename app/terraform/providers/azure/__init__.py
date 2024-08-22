import os

from jinja2 import Environment, FileSystemLoader

from app.classes import Network, Subnet, Host, Config


class TerraformAzure:
    def __init__(self):
        self.environment = Environment(
            loader=FileSystemLoader(
                os.path.join(os.path.dirname(__file__), "templates/")
            )
        )

    def _provision_config(self):
        template = self.environment.get_template("config.j2")
        content = template.render()
        return content

    def _provision_project(self, project_name: str, location: str):
        template = self.environment.get_template("resource_group.j2")
        content = template.render(
            resource_group_id=project_name,
            resource_group_name=project_name,
            resource_group_location=location,
        )
        return content

    def _provision_network(self, network: Network, project_name: str):
        template = self.environment.get_template("network.j2")
        content = template.render(
            network_id=project_name,
            network_name=project_name,
            network_cidr=network.cidr,
            resource_group_id=project_name,
        )
        return content

    def _provision_subnet(self, subnet: Subnet, project_name: str):
        template = self.environment.get_template("subnet.j2")
        content = template.render(
            subnet_id=subnet.name,
            subnet_name=subnet.name,
            subnet_cidr=subnet.cidr,
            network_id=project_name,
            resource_group_id=project_name,
        )
        return content

    def _provision_vm(self, host: Host, project_name: str, public: bool = False):
        # TODO: variable os, size and disk
        template = self.environment.get_template("vm.j2")
        content = template.render(
            vm_id=host.name,
            vm_name=host.name,
            vm_size="Standard_B1s",
            vm_username=host.username,
            vm_password=host.password,
            vm_ip=host.ip,
            vm_os_publisher="Canonical",
            vm_os_offer="UbuntuServer",
            vm_os_sku="18.04-LTS",
            vm_os_version="latest",
            vm_disk_type="Standard_LRS",
            resource_group_id=project_name,
            subnet_id=host.subnet,
            public_ip=public,
        )
        return content

    def provision(
        self,
        config: Config,
    ):
        content = []

        content.append(self._provision_config())

        content.append(
            self._provision_project(config.project.name, config.project.location)
        )

        content.append(self._provision_network(config.network, config.project.name))

        for subnet in config.subnets:
            content.append(self._provision_subnet(subnet, config.project.name))

        for host in config.hosts:
            content.append(self._provision_vm(host, config.project.name))

        # TODO: VPN VM parameters
        # TODO: public ip
        content.append(
            self._provision_vm(
                Host(
                    name="vpn",
                    username="vpn",
                    password="soj893f4hIYa!",
                    ip=config.vpn.lan_ip,
                    subnet=config.vpn.subnet,
                ),
                config.project.name,
                public=True,
            )
        )

        return "\n\n".join(content)
