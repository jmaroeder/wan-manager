import logging
import re
from abc import ABC


class Isp(ABC):
    name: str
    pattern: re.Pattern

    def __init__(self) -> None:
        self.log = logging.getLogger(f"{__name__}:{self.__class__.__name__}")

    async def on_connect(self) -> None:
        self.log.info("Connected to %s", self.name)

    async def on_disconnect(self) -> None:
        self.log.info("Disconnected from %s", self.name)

    def __str__(self) -> str:
        return f"Isp({self.name})"
