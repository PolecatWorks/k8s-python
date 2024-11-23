from aiohttp import web
from k8spython.service import service_app_create
from k8spython.config import ServiceConfig

import pytest
import pytest_asyncio


async def hello(request):
    return web.Response(text='Hello, world')


async def test_hello(aiohttp_client):
    app = web.Application()
    app.router.add_get('/', hello)
    client = await aiohttp_client(app)
    resp = await client.get('/')
    assert resp.status == 200
    text = await resp.text()
    assert 'Hello, world' in text


# @pytest_asyncio.fixture
# async def server(aiohttp_server):
#     app = web.Application()
#     return await aiohttp_server(app)


@pytest.fixture
def config() -> ServiceConfig:
    file = """
---
webservice:
  url: http://localhost:8080
  prefix: pie/v0
hams:
  url: http://localhost:8079
  prefix: hams
"""

    with open("tests/test_data/config.yaml", "rb") as config_file:
        config = config_parse(config_file)
        return config



@pytest_asyncio.fixture
async def client(aiohttp_client, config):
    app = web.Application()
    service_app_create(app, config)
    return await aiohttp_client(app)


async def test_apple(client):
    response = await client.get('/pie/v0/apple')
    assert response.status == 200
    text = await response.text()
    assert 'Apple' in text
    assert response.content_type == 'application/json'
    json_data = await response.json()
    assert json_data == {"fruit": "Apple"}
