from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from pathlib import Path

import httpx
from fastapi import FastAPI

from final_project.infrastructure.github_client import GitHubClient


@asynccontextmanager
async def lifespan_setup(app: FastAPI) -> AsyncGenerator[None]:
    """
    Actions to run on application startup.

    This function uses fastAPI app to store data
    in the state, such as db_engine.

    :param app: the fastAPI application.
    :return: function that actually performs actions.
    """
    Path("static").mkdir(exist_ok=True)

    http_client = httpx.AsyncClient(
        timeout=30.0,
        limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
    )
    app.state.http_client = http_client

    github_client = GitHubClient(http_client=http_client)
    app.state.github_client = github_client

    app.middleware_stack = None
    app.middleware_stack = app.build_middleware_stack()

    yield

    await http_client.aclose()
