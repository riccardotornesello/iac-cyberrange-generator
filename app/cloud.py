import sys

from .providers.azure import Azure


def configure_provider(cloud: dict):
    if cloud["provider"] == "azure":
        return Azure(cloud["options"])
    else:
        print("This provider is not supported")
        sys.exit(1)
