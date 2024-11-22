import logging.config

from dependency_injector import containers, providers

from .isp.isp_detector import IspDetector
from .isp.starlink import Starlink
from .isp.zito import Zito
from .sabnzbd_client import SabnzbdClient


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[".", ".isp.isp_detector", ".isp.starlink", ".isp.zito"],
    )

    config = providers.Configuration(yaml_files=["config.yaml"])

    logging = providers.Resource(
        logging.config.fileConfig,
        fname="logging.ini",
    )

    sabnzbd_client = providers.Singleton(
        SabnzbdClient,
        api_key=config.sabnzbd.api_key,
        base_url=config.sabnzbd.base_url,
    )

    starlink = providers.Singleton(Starlink)
    zito = providers.Singleton(Zito)
    isps = providers.List(starlink, zito)

    isp_detector = providers.Singleton(
        IspDetector,
        # isps=isps,
    )
