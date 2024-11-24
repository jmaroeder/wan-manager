import logging
import sys

from dependency_injector import providers, resources
from dependency_injector.wiring import Provide, inject


class Logging(resources.Resource):
    @inject
    def init(self, config: providers.Configuration = Provide["config"]) -> None:
        logging.basicConfig(
            stream=sys.stdout,
            level=config["log"]["level"],
            format=config["log"]["format"],
        )

        for name, level in config["log"]["levels"].items():
            logging.getLogger(name).setLevel(level)
