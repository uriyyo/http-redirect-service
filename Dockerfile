FROM python:3.12.1-slim as requirements-stage

WORKDIR /tmp

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN pip install poetry
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12.1-slim

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt

RUN pip install -U -r /app/requirements.txt

COPY ./pyproject.toml ./poetry.lock ./start.sh /app/
COPY ./configs /app/configs
COPY ./http_redirect_service /app/http_redirect_service

CMD ["/app/start.sh"]
