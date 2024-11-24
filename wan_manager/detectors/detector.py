import logging
from abc import ABC, abstractmethod
from datetime import timedelta


class Detector[T](ABC):
    name: str

    def __init__(self, freq: timedelta | None = None) -> None:
        self.log = logging.getLogger(f"{__name__}:{self.__class__.__name__}")
        self.freq = freq or timedelta(seconds=30)
        self.last_value: T = None

    async def run_once(self) -> T:
        self.log.info("Detecting with %s", self.name)
        new_value = await self.detect()
        if new_value != self.last_value:
            new_value = await self.on_change(new_value, self.last_value)
            self.last_value = new_value

    async def on_change(self, new_value: T, old_value: T) -> T:
        self.log.info("Changed from %s to %s", old_value, new_value)

    @abstractmethod
    async def detect(self) -> T:
        pass
