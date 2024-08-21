import os

from app.terraform.providers.azure import TerraformAzure
from app.classes import Network, Subnet, Host


if __name__ == "__main__":
    terraform = TerraformAzure()

    project_name = "cyberrange"
    location = "West Europe"

    network = Network(cidr="10.0.0.0/16")
    subnets = [Subnet(name="main", cidr="10.0.1.0/24")]
    hosts = [
        Host(
            name="manager",
            username="testadmin",
            password="testAdmin1234!",
            ip="10.0.1.5",
            subnet="main",
        )
    ]

    with open("test.tf", "w") as f:
        f.write(terraform.provision(project_name, location, network, subnets, hosts))
