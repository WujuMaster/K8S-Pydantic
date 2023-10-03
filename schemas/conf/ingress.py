from typing import List, Optional

from pydantic import BaseModel


class IngressConfTls(BaseModel):
    secretName: str
    hosts: List[str]


class IngressConfMetaData(BaseModel):
    annotations: Optional[dict] = None


class IngressConfPlugin(BaseModel):
    name: str


class IngressConf(BaseModel):
    pathType: str
    tls: Optional[IngressConfTls] = None
    name: str
    className: str
    metadata: IngressConfMetaData
    plugin: IngressConfPlugin
