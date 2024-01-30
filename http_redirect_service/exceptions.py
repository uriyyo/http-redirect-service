from typing import Any

from fastapi import HTTPException, status


class BaseRedirectServiceException(HTTPException):
    default_detail: str
    default_status_code: int

    def __init__(
        self,
        *,
        detail: str | None = None,
        status_code: int | None = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            detail=detail or self.default_detail,
            status_code=status_code or self.default_status_code,
            **kwargs,
        )


class RedisClientIsNotInitializedException(BaseRedirectServiceException):
    default_detail = "Redis client is not initialized"
    default_status_code = status.HTTP_500_INTERNAL_SERVER_ERROR


class UnknownPoolIDException(BaseRedirectServiceException):
    default_detail = "Unknown pool-id"
    default_status_code = status.HTTP_404_NOT_FOUND


__all__ = [
    "BaseRedirectServiceException",
    "RedisClientIsNotInitializedException",
    "UnknownPoolIDException",
]
