import re
from datetime import time

from dependency_injector.wiring import Provide, inject

from wan_manager.sabnzbd_client import SabnzbdClient

from .isp import Isp


class Starlink(Isp):
    name = "Starlink"
    pattern = re.compile(r"starlink", re.IGNORECASE)
    offpeak_start = time.fromisoformat("04:00:00")
    offpeak_end = time.fromisoformat("11:00:00")

    @inject
    def __init__(
        self, sabnzbd_client: SabnzbdClient = Provide["sabnzbd_client"]
    ) -> None:
        super().__init__()
        self.sabnzb_client = sabnzbd_client

    def on_connect(self) -> None:
        super().on_connect()
        self.sabnzb_client.resume()
        self.sabnzb_client.set_schedule(self.offpeak_end, self.offpeak_start)

    def on_disconnect(self) -> None:
        super().on_disconnect()
        self.sabnzb_client.clear_schedule()
