FROM python:3.13.0-slim-bookworm as build

RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# RUN pip3 install poetry

COPY * ./
COPY k8spython k8spython
RUN pip3 install .

FROM python:3.13.0-slim-bookworm as publish
COPY --from=build /opt/venv /opt/venv

ENV VIRTUAL_ENV=/opt/venv
ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ["k8s-python"]
