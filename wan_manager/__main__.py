import asyncio
import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from dependency_injector.wiring import inject

from .containers import Container

log = logging.getLogger(__name__)


@asynccontextmanager
async def container_context() -> AsyncGenerator[Container]:
    container = Container()
    await container.init_resources()
    yield container
    await container.shutdown_resources()


@inject
async def async_main() -> None:
    async with container_context() as container:
        await container.dispatcher().run()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main()
