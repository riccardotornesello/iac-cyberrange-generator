import sys

from . import providers


def configure_provider(cloud: dict):
    if cloud["provider"] == "azure":
        return providers.Azure(cloud["options"])
    else:
        print("This provider is not supported")
        sys.exit(1)
