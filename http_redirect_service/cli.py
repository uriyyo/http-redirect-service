import json
from pathlib import Path
from typing import Annotated, cast

import click
import uvicorn
from annotated_types import Len
from loguru import logger
from pydantic import TypeAdapter
from redis import Redis

from http_redirect_service.app import get_app
from http_redirect_service.models import PoolDomains, PoolID
from http_redirect_service.settings import settings


@click.group()
def cli() -> None:
    pass


@cli.command()
def debug() -> None:  # to run app locally
    uvicorn.run(get_app())


_PollConfig = Annotated[
    dict[PoolID, PoolDomains],
    Len(min_length=1),
]
_PoolConfigAdapter = TypeAdapter(_PollConfig)


@cli.command(name="sync-config")
@click.option(
    "-c",
    "--config",
    type=click.Path(exists=True, dir_okay=False, resolve_path=True),
)
def sync_config(config: str) -> None:
    with Path(config).open() as f:
        data = json.load(f)
        validated_config = _PoolConfigAdapter.validate_python(data)

    redis_client = cast(Redis, Redis.from_url(str(settings.REDIS_DSN)))

    with redis_client, redis_client.pipeline() as pipe:
        pipe.flushall()
        for pool_id, pool_domains in validated_config.items():
            pipe.zadd(pool_id, pool_domains)
        pipe.execute()  # type: ignore[no-untyped-call]

    logger.info("Config has been synced")


if __name__ == "__main__":
    cli()
