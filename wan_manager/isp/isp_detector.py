import logging
from collections.abc import Collection

import requests
from dependency_injector.wiring import Provide, inject

from .isp import Isp


class IspDetector:
    @inject
    def __init__(self, isps: Collection[Isp] = Provide["isps"]) -> None:
        self.isps = isps
        self.current_isp: Isp = None
        self.log = logging.getLogger(
            f"{__name__}.{self.__class__.__name__}",
        )

    def detect_isp(self) -> Isp:
        self.log.info("Detecting ISP")
        response = requests.get("http://ip-api.com/json/", {"fields": "isp"})
        data = response.json()
        self.log.debug(f"Response: {data["isp"]}")
        for isp in self.isps:
            self.log.debug(f"Checking {isp}")
            if isp.pattern.search(data["isp"]):
                return isp
        return None

    def update_isp(self) -> None:
        isp = self.detect_isp()
        if isp != self.current_isp:
            if self.current_isp:
                self.current_isp.on_disconnect()
            if isp:
                isp.on_connect()
            self.current_isp = isp
        return self.current_isp
