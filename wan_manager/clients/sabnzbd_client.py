import logging
from collections.abc import Awaitable, Mapping
from datetime import time
from enum import Enum, auto
from urllib.parse import urljoin

from aiohttp import ClientResponse
from dependency_injector.wiring import Provide, inject

from wan_manager.clients.http_client import HttpClient


class Schedline(Enum):
    ENABLED = auto()
    DISABLED = auto()


class SabnzbdClient:
    @inject
    def __init__(
        self,
        api_key: str,
        base_url: str,
        http_client: HttpClient = Provide["http_client"],
    ) -> None:
        self.log = logging.getLogger(f"{__name__}:{self.__class__.__name__}")
        self.api_key = api_key
        self.base_url = base_url
        self.api_url = urljoin(base_url, "/api")
        self.params = {"apikey": api_key, "output": "json"}
        self.http_client = http_client

    async def call(self, **params: Mapping[str, str]) -> Awaitable[ClientResponse]:
        self.log.debug("call(%s)", params)
        return await self.http_client.get(
            self.api_url, params={**self.params, **params}
        )

    async def clear_schedule(self) -> None:
        """Clears any scheduled pause and resume times."""
        await self.call(mode="config", keyword="schedlines", value="")

    async def set_schedule(self, pause_time: time, resume_time: time) -> None:
        """Schedules pause and resume times for Sabnzbd. Times are in server time, which is UTC."""
        await self.call(
            mode="config",
            keyword="schedlines",
            value=",".join(
                [
                    self.build_schedline(pause_time, "pause"),
                    self.build_schedline(resume_time, "resume"),
                ]
            ),
        )

    async def pause(self) -> None:
        """Pauses Sabnzbd."""
        await self.call(mode="pause")

    async def resume(self) -> None:
        """Resumes Sabnzbd."""
        await self.call(mode="resume")

    @staticmethod
    def build_schedline(d: time, action: str, schedline: Schedline) -> str:
        """Builds a schedline for Sabnzbd."""
        return " ".join(
            [
                "1" if schedline == Schedline.ENABLED else "0",  # enabled
                f"{d.minute}",  # minute
                f"{d.hour}",  # hour
                "1234567",  # days of week
                action,  # action
            ]
        )
