import logging
from collections.abc import Mapping
from datetime import time
from enum import Enum, auto
from urllib.parse import urljoin

import requests


class Schedline(Enum):
    ENABLED = auto()
    DISABLED = auto()


class SabnzbdClient:
    def __init__(self, api_key: str, base_url: str) -> None:
        self.log = logging.getLogger(f"{__name__}.{self.__class__.__name__}")
        self.api_key = api_key
        self.base_url = base_url
        self.api_url = urljoin(base_url, "/api")
        self.params = {"apikey": api_key, "output": "json"}

    def call(self, **params: Mapping[str, str]) -> requests.Response:
        self.log.debug("call(%s)", params)
        return requests.get(self.api_url, params={**self.params, **params})

    def clear_schedule(self) -> None:
        """Clears any scheduled pause and resume times."""
        self.call(mode="config", keyword="schedlines", value="")

    def set_schedule(self, pause_time: time, resume_time: time) -> None:
        """Schedules pause and resume times for Sabnzbd. Times are in server time, which is UTC."""
        self.call(
            mode="config",
            keyword="schedlines",
            value=",".join(
                [
                    self.build_schedline(pause_time, "pause"),
                    self.build_schedline(resume_time, "resume"),
                ]
            ),
        )

    def pause(self) -> None:
        """Pauses Sabnzbd."""
        self.call(mode="pause")

    def resume(self) -> None:
        """Resumes Sabnzbd."""
        self.call(mode="resume")

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
