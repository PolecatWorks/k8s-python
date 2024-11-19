# Description: Dockerfile for building the k8s-python container

FROM python:3.13.0-slim-bookworm AS base

FROM base AS build


RUN apt-get update
RUN apt-get update --fix-missing && apt-get install -y --fix-missing \
    build-essential \
    gcc \
    g++ \
    cmake \
    autoconf && \
    rm -rf /var/lib/apt/lists/* && \
    mkdir /install

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

WORKDIR /app
COPY * ./
COPY k8spython k8spython

RUN pip3 install .

# Entrypoint is here in case we want to run the build layer as a standalone container
ENTRYPOINT ["/bin/sh"]

FROM base AS publish
EXPOSE 8080 8079
COPY --from=build /opt/venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["k8s-python"]
