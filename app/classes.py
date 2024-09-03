from dataclasses import dataclass
from typing import List


@dataclass
class Project:
    name: str
    location: str


@dataclass
class Network:
    cidr: str


@dataclass
class Subnet:
    name: str
    cidr: str


@dataclass
class Service:
    name: str


@dataclass
class Host:
    name: str
    username: str
    password: str
    ip: str
    subnet: str
    services: List[Service]


@dataclass
class Vpn:
    subnet: str
    lan_ip: str
    vpn_subnet: str


@dataclass
class Config:
    project: Project
    network: Network
    subnets: list[Subnet]
    hosts: list[Host]
    vpn: Vpn
