import os
import shutil
from datetime import datetime
from Crypto.PublicKey import RSA

from . import settings


variable_folders = ["env", "inventory"]


def move_old():
    date_time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    backup_folder = os.path.join(".backup", date_time)

    for folder in variable_folders:
        folder_full_path = os.path.join(settings.PRIVATE_DATA_DIR, folder)
        if os.path.exists(folder_full_path) and len(os.listdir(folder_full_path)) > 0:
            os.makedirs(backup_folder, exist_ok=True)
            shutil.move(folder_full_path, os.path.join(backup_folder, folder))

    provisioning_full_path = os.path.join(settings.PRIVATE_DATA_DIR, "project/provisioning.yml")
    if os.path.exists(provisioning_full_path):
        os.makedirs(os.path.join(backup_folder, "project"), exist_ok=True)
        shutil.move(provisioning_full_path, os.path.join(backup_folder, "project/provisioning.yml"))


def create_folders():
    for folder in variable_folders:
        folder_full_path = os.path.join(settings.PRIVATE_DATA_DIR, folder)
        os.makedirs(folder_full_path, exist_ok=True)


def generate_keys():
    if os.path.exists("./keys/private.key"):
        return

    key = RSA.generate(2048)
    with open("keys/private.key", 'wb') as content_file:
        content_file.write(key.exportKey('PEM'))
    os.chmod("keys/private.key", 0o600)
    pubkey = key.publickey()
    with open("keys/public.key", 'wb') as content_file:
        content_file.write(pubkey.exportKey('OpenSSH'))


def generate_hosts(manager, vulnboxes):
    with open(".public_ip") as f:
        public_ip = f.readline().strip()

    hosts_lines = [
        "[manager]",
        f"{public_ip} ansible_connection=ssh ansible_user={manager['username']} ansible_ssh_pass={manager['password']}",
        "[vulnbox]"
    ]

    for vulnbox in vulnboxes:
        hosts_lines.append(f"{vulnbox['hostname']} ansible_host={vulnbox['ip']} ansible_connection=ssh ansible_user={vulnbox['username']} ansible_ssh_pass={vulnbox['password']}")

    hosts_lines.extend([
        "[vulnbox:vars]",
        f"ansible_ssh_common_args='-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o ProxyCommand=\"ssh -W %h:%p -i keys/private.key -q {manager['username']}@{public_ip}\"'"
    ])

    with open("ansible/inventory/hosts", "w") as f:
        f.write('\n'.join(hosts_lines))
