
from pydantic import Field, BaseModel
from pydantic import HttpUrl


class HamsConfig(BaseModel):
    url: HttpUrl = Field(description="Host to listen for health and monitoring")
    prefix: str = Field(description="Prefix for the name of the resources")
