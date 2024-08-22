# Design and development of a tool for the implementation of cloud-based cyber ranges with open source software ​

## Description

This project is the Proof of Concept of my Bachelor degree's thesis. It uses Ansible to generate a cyber-range using the Infrastructure as Code paradigm. It will be slowly updated to add new features, use Terraform for the provisioning stage, fix bugs and clean the code.

## Project status

The previous version of the PoC using only Ansible ends at commit [9263cd44c78e1b34315ea65730ee230ab36b983b](https://github.com/riccardotornesello/iac-cyberrange-generator/tree/9263cd44c78e1b34315ea65730ee230ab36b983b).
However, the project is currently being restructured to give it new life after changes in the tools made it obsolete. This version uses Terraform for provisioning and Ansible for virtual machine configuration.

At the moment the tool works for the provisioning part but the configuration of services is still work in progress and will be finished in the future with sporadic updates.

## Deployment and compatibility

This tool is designed to be cloud-agnostic: no matter which cloud provider you intend to use, the syntax will always be the same.

In the current implementation (PoC), the only cloud provider supported is Microsoft Azure.

Moreover, at present this tool only allows you to create Linux virtual machines.

## How to run

First, you need to install the dependencies:

```bash
pip3 install -r requirements.txt
```

Then, you need to create a configuration file. You can update the `config.yml` file with your own values.

Finally, you can run the tool with the following commands:

- To create the infrastructure: `python3 main.py`
- To delete the infrastructure: `python3 main.py destroy`
- To rebuild it after updates in the services: `python3 main.py rebuild`
