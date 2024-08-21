from dataclasses import dataclass


@dataclass
class Network:
    cidr: str


@dataclass
class Subnet:
    name: str
    cidr: str


@dataclass
class Host:
    name: str
    username: str
    password: str
    ip: str
    subnet: str
