

from pydantic import Field, BaseModel
from pydantic import HttpUrl


# TODO: Look here in future: https://github.com/pydantic/pydantic/discussions/2928#discussioncomment-4744841
class WebServerConfig(BaseModel):
    """
    Configuration for the web server
    """
    url: HttpUrl = Field(description="Host to listen on")
    prefix: str = Field(description="Prefix for the name of the resources")


class ServiceConfig(BaseModel):
    """
    Configuration for the service
    """
    web: WebServerConfig = Field(description="Web server configuration")
