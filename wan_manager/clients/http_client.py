from collections.abc import AsyncGenerator
from contextlib import AbstractAsyncContextManager
from datetime import timedelta
from typing import Any

from aiohttp import ClientResponse, ClientSession, ClientTimeout
from dependency_injector import providers
from dependency_injector.wiring import Provide, inject


class HttpClient:
    @inject
    def __init__(
        self,
        client_session_provider: providers.Resource[ClientSession] = Provide[
            "client_session.provider"
        ],
    ) -> None:
        self.client_session_provider = client_session_provider
        self.client_session: ClientSession | None = None

    async def request(
        self, method: str, url: str, **kwargs: Any
    ) -> AbstractAsyncContextManager[ClientResponse]:
        if self.client_session is None:
            self.client_session = await self.client_session_provider()
        return await self.client_session.request(method, url, **kwargs)

    async def get(
        self, url: str, **kwargs: Any
    ) -> AbstractAsyncContextManager[ClientResponse]:
        return await self.request("GET", url, **kwargs)


async def init_client_session(
    default_timeout: timedelta = timedelta(seconds=10),
) -> AsyncGenerator[ClientSession]:
    client_session = ClientSession(
        timeout=ClientTimeout(total=default_timeout.total_seconds())
    )
    yield client_session
    await client_session.close()
