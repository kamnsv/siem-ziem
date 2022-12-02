FROM python:3.9-slim-buster

COPY ./dist /dist

WORKDIR /var/log/ziem
WORKDIR /var/opt/ziem

RUN pip install /dist/*/*