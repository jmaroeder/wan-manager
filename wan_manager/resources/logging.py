import logging
import os
import sys

from dependency_injector import providers, resources
from dependency_injector.wiring import Provide, inject


class Logging(resources.Resource):
    @inject
    def init(self, config: providers.Configuration = Provide["config"]) -> None:
        logging.basicConfig(
            stream=sys.stdout,
            level=os.getenv("WAN_MANAGER_LOG_LEVEL", config["log"]["level"]),
            format=os.getenv("WAN_MANAGER_LOG_FORMAT", config["log"]["format"]),
        )

        for name, level in config["log"]["levels"].items():
            logging.getLogger(name).setLevel(level)
