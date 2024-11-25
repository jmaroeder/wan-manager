import os

from dependency_injector import containers, providers

from wan_manager.clients.http_client import HttpClient, init_client_session
from wan_manager.dispatcher import Dispatcher
from wan_manager.resources.logging import Logging

from .clients.sabnzbd_client import SabnzbdClient
from .detectors.isp_detector import IspDetector
from .isps.starlink import Starlink
from .isps.zito import Zito


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[".", ".detectors.isp_detector", ".isps.starlink", ".isps.zito"],
    )

    config = providers.Configuration(yaml_files=["config.yaml"])
    logging = providers.Resource(Logging)

    client_session = providers.Resource(init_client_session)

    http_client = providers.Factory(HttpClient)

    sabnzbd_client = providers.Singleton(
        SabnzbdClient,
        api_key=os.getenv("WAN_MANAGER_SABNZBD_API_KEY", config.sabnzbd.api_key),
        base_url=os.getenv("WAN_MANAGER_SABNZBD_BASE_URL", config.sabnzbd.base_url),
    )

    starlink = providers.Singleton(Starlink)
    zito = providers.Singleton(Zito)
    isps = providers.List(starlink, zito)

    isp_detector = providers.Singleton(IspDetector)
    detectors = providers.List(isp_detector)

    dispatcher = providers.Factory(Dispatcher)
