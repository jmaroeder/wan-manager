from collections.abc import Collection, Mapping
from datetime import timedelta

from dependency_injector.wiring import Provide, inject

from wan_manager.clients.http_client import HttpClient

from ..isps.isp import Isp
from .detector import Detector


class IspDetector(Detector[Isp]):
    name = "IspDetector"

    @inject
    def __init__(
        self,
        isps: Collection[Isp] = Provide["isps"],
        http_client: HttpClient = Provide["http_client"],
        freq: timedelta | None = None,
    ) -> None:
        super().__init__(freq)
        self.isps = isps
        self.http_client = http_client
        self.current_isp: Isp = None
        # self.log = logging.getLogger(
        #     f"{__name__}:{self.__class__.__name__}",
        # )

    async def detect(self) -> Isp:
        async with await self.http_client.get(
            "http://ip-api.com/json/", params={"fields": "isp"}
        ) as response:
            data: Mapping = await response.json()
        self.log.debug(f"Response: {data["isp"]}")
        for isp in self.isps:
            if isp.pattern.search(data["isp"]):
                return isp
        return None

    async def on_change(self, new_value: Isp, old_value: Isp) -> Isp:
        await super().on_change(new_value, old_value)
        if old_value:
            await old_value.on_disconnect()
        if new_value:
            await new_value.on_connect()
        return new_value
