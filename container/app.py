# This file enables support for adev during development. It is not required for the application to run.
from k8spython.service import service_start

if __name__ == '__main__':
    with open("config.yaml", "rb") as config_file:
        service_start(config_file)
