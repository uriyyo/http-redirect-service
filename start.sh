#!/usr/bin/env bash

exec uvicorn        \
    --host 0.0.0.0  \
    --port 80       \
    --access-log    \
    --loop="uvloop" \
    --proxy-headers \
    --factory       \
    --workers 5     \
    http_redirect_service.app:get_app
