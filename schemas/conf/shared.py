from pydantic import BaseModel


class SharedConfImage(BaseModel):
    registry: str
    tag: str = "latest"


class SharedConf(BaseModel):
    replicas: int = 1
    namespace: str = "default"
    image: SharedConfImage
    version: int = 0
