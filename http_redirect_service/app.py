from asgi_correlation_id import CorrelationIdMiddleware
from fastapi import FastAPI
from fastapi_async_safe import init_app
from prometheus_client import make_asgi_app
from starlette.middleware import Middleware

from .dependencies import redis_lifespan
from .logging_config import configure_logging
from .routes import router
from .settings import settings

configure_logging()


def get_app() -> FastAPI:
    docs_kwargs = (
        {
            "redoc_url": None,
            "docs_url": None,
            "openapi_url": None,
        }
        if settings.is_prod
        else {}
    )

    app = FastAPI(
        title="HTTP Redirect Service",
        version="0.1.0",
        lifespan=redis_lifespan,
        debug=not settings.is_prod,
        middleware=[
            Middleware(CorrelationIdMiddleware),
        ],
        **docs_kwargs,  # type: ignore[arg-type]
    )
    app.mount("/metrics", make_asgi_app())
    app.include_router(router)

    if not settings.is_test:
        init_app(app)

    return app


__all__ = [
    "get_app",
]
