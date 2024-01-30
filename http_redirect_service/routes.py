from typing import Annotated

from fastapi import APIRouter, Depends, Header, Path, Request, Response, status
from loguru import logger
from pydantic import BaseModel
from redis.asyncio import Redis
from starlette.responses import RedirectResponse

from .dependencies import PoolService, get_redis_client
from .exceptions import UnknownPoolIDException
from .models import PoolID

router = APIRouter()


class HealthCheckResponseModel(BaseModel):
    redis: bool


@router.get("/_healthcheck")
async def healthcheck(
    response: Response,
    redis_client: Annotated[Redis, Depends(get_redis_client)],
) -> HealthCheckResponseModel:
    redis_available = await redis_client.ping()

    if not redis_available:
        logger.error("Redis is not available")
        response.status_code = status.HTTP_503_SERVICE_UNAVAILABLE

    return HealthCheckResponseModel(
        redis=redis_available,
    )


@router.api_route(
    path="/{path:path}",
    methods=[
        "GET",
        "POST",
        "PUT",
        "PATCH",
        "DELETE",
        "OPTIONS",
        "HEAD",
    ],
)
async def redirect_requests(
    request: Request,
    path: Annotated[str, Path(...)],
    x_pool_id: Annotated[PoolID, Header(..., alias="X-Pool-ID")],
    pool_service: Annotated[PoolService, Depends()],
) -> RedirectResponse:
    redirect_result = await pool_service.get_redirect_domain(x_pool_id)

    if redirect_result is None:
        logger.error("Unknown pool-id: {}", x_pool_id)
        raise UnknownPoolIDException

    domain, weight = redirect_result

    logger.info(
        "Redirecting from {} (pool-id: {}) to {} domain (weight {})",
        request.url,
        x_pool_id,
        domain,
        weight,
    )

    return RedirectResponse(
        request.url.replace(netloc=domain),
        status_code=status.HTTP_307_TEMPORARY_REDIRECT,
    )


__all__ = [
    "router",
]
