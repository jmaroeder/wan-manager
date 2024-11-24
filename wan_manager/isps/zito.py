import re

from dependency_injector.wiring import Provide, inject

from wan_manager.clients.sabnzbd_client import SabnzbdClient

from .isp import Isp


class Zito(Isp):
    name = "Zito"
    pattern = re.compile(r"zito", re.IGNORECASE)

    @inject
    def __init__(
        self, sabnzbd_client: SabnzbdClient = Provide["sabnzbd_client"]
    ) -> None:
        super().__init__()
        self.sabnzb_client = sabnzbd_client

    async def on_connect(self) -> None:
        await super().on_connect()
        await self.sabnzb_client.resume()
