# Design and development of a tool for the implementation of cloud-based cyber ranges with open source software ​

## Description

This project is the Proof of Concept of my Bachelor degree's thesis. It uses Ansible to generate a cyber-range using the Infrastructure as Code paradigm. It will be slowly updated to add new features, use Terraform for the provisioning stage, fix bugs and clean the code.

## Deployment and compatibility

This tool is designed to be cloud-agnostic: no matter which cloud provider you intend to use, the syntax will always be the same.

In the current implementation (POC), the only cloud provider supported is Microsoft Azure.

## Directory tree

```
├── ansible
│   ├── project: generated ansible playbooks
│       ├── roles: required and downloaded ansible roles
├── app: tool Python code
├── keys: where the generated ssh keys are stored
├── static: files required by the services to be installed in the VMs
├── config.yml: cyber range configuration file
└── main.py: tool entrypoint
```

## How to run

`python3 -m main`
