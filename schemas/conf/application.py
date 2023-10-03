from typing import Any, Dict, List, Optional

from pydantic import BaseModel


class ImageConf(BaseModel):
    repository: str
    tag: str
    containerPort: int


class DeploymentConf(BaseModel):
    replicas: int


class ServiceConf(BaseModel):
    port: int


class AppIngressConf(BaseModel):
    host: Optional[str] = None
    path: str
    pathType: Optional[str] = "Prefix"


class ApplicationConf(BaseModel):
    name: str
    image: ImageConf
    deployment: DeploymentConf
    service: ServiceConf
    ingress: List[AppIngressConf]
    env: List[str] = []
    secret: List[str] = []


class ApplicationConfList(BaseModel):
    applications: List[ApplicationConf]
