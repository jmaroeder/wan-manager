import logging

from dependency_injector.wiring import Provide, inject

from .containers import Container

log = logging.getLogger(__name__)


@inject
def main(container: Container = Provide[Container]) -> None:
    isp_detector = container.isp_detector()
    isp = isp_detector.update_isp()
    log.info("detected %s", isp)


container = Container()
container.wire(modules=[__name__])
container.init_resources()

if __name__ == "__main__":
    main()
