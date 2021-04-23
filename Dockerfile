FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

LABEL maintainer="Joseph Rocky Holms <joseph.holms@yahoo.com>"

WORKDIR /app

COPY poetry.lock pyproject.toml /app/

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install

COPY . /app/

ENV MODULE_NAME="src.api.main"
ENV APP_MODULE="src.api.main:APP"