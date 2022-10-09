# DEV STAGE
FROM python:3.9-slim as dev

ENV STAGE=DEV

ENV PYTHONDONTWRITEBYTECODE 1

RUN apt update && apt -y upgrade

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

WORKDIR /api

CMD uvicorn main:app --reload --host 0.0.0.0

# PROD STAGE
FROM dev as prod

ENV STAGE=PROD

COPY ./api /api

CMD uvicorn main:app --reload --host 0.0.0.0


