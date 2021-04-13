import os
import shutil
from datetime import datetime

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


def create_folders():
    for folder in variable_folders:
        folder_full_path = os.path.join(settings.PRIVATE_DATA_DIR, folder)
        os.makedirs(folder_full_path, exist_ok=True)
