import sys
import yaml

from app import init, cloud

if __name__ == "__main__":
    with open("config.yml", "r") as stream:
        try:
            config = yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)
            sys.exit(1)

    init.move_old()
    init.create_folders()

    provider = cloud.configure_provider(config["cloud"])
