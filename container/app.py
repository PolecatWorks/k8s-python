# This file enables support for adev during development. It is not required for the application to run.
from k8spython.service import config_parse, service_app_create, service_init, service_start
from aiohttp import web



def create_app():
    print("Starting service")
    # logging.basicConfig(level=logging.DEBUG)

    app = web.Application()

    with open("tests/test_data/config.yaml", "rb") as config_file:
        app = service_init(app, config_file)


    return app
