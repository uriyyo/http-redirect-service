from logging.config import dictConfig

from .settings import settings

BASIC_LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "level": "DEBUG" if not settings.is_prod else "INFO",
    "filters": {
        "correlation_id": {
            "()": "asgi_correlation_id.CorrelationIdFilter",
            "uuid_length": 32,
            "default_value": "-",
        },
    },
    "formatters": {
        "access": {
            "()": "uvicorn.logging.AccessFormatter",
            "fmt": "%(levelprefix)s %(asctime)s | [%(correlation_id)s] |"
            " %(client_addr)s | %(request_line)s %(status_code)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": False,
        },
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": "%(levelprefix)s %(asctime)s | [%(correlation_id)s] | %(name)s | %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
            "use_colors": False,
        },
    },
    "handlers": {
        "file": {
            # TODO: simple one, can be replaced with TimedRotatingFileHandler
            "class": "logging.FileHandler",
            "formatter": "default",
            "filename": "http_redirect_service.log",
            "mode": "a",
            "filters": ["correlation_id"],
        },
        "access": {
            "class": "logging.StreamHandler",
            "formatter": "access",
            "stream": "ext://sys.stdout",
            "filters": ["correlation_id"],
        },
        "default": {
            "class": "logging.StreamHandler",
            "formatter": "default",
            "stream": "ext://sys.stderr",
            "filters": ["correlation_id"],
        },
    },
    "loggers": {
        "http_redirect_service": {
            "handlers": ["default", "file"],
            "level": "DEBUG",
            "propagate": True,
        },
        "uvicorn": {
            "level": "INFO",
            "propagate": True,
        },
        "uvicorn.access": {
            "handlers": ["access", "file"],
            "level": "INFO",
            "propagate": True,
        },
        "uvicorn.error": {
            "handlers": ["default", "file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}


def configure_logging() -> None:
    if settings.is_test:
        return

    dictConfig(BASIC_LOGGING_CONFIG)


__all__ = [
    "configure_logging",
]
