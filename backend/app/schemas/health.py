from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(examples=["ok"])
    env: str
    service: str


class ApiInfoResponse(BaseModel):
    name: str
    version: str = "v1"
    env: str
