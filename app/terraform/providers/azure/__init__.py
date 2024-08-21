import os
from typing import List

from jinja2 import Environment, FileSystemLoader

from app.classes import Network, Subnet, Host


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

    def _provision_vm(self, host: Host, project_name: str):
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
        )
        return content

    def provision(
        self,
        project_name: str,
        location: str,
        network: Network,
        subnets: List[Subnet],
        hosts: List[Host],
    ):
        content = [self._provision_config()]
        content.append(self._provision_project(project_name, location))
        content.append(self._provision_network(network, project_name))
        for subnet in subnets:
            content.append(self._provision_subnet(subnet, project_name))
        for host in hosts:
            content.append(self._provision_vm(host, project_name))

        return "\n\n".join(content)
