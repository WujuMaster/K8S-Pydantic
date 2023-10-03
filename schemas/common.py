from typing import Dict, Literal, Optional

from pydantic import BaseModel


class LabelSelector(BaseModel):
    matchLabels: Dict[str, str]


class PodMetaData(BaseModel):
    labels: Dict[str, str]


class CommonMetaData(PodMetaData):
    name: str
    namespace: Optional[str] = None


class DeploymentMetaData(CommonMetaData):
    pass


class ServiceMetaData(CommonMetaData):
    pass


class IngressMetaData(CommonMetaData):
    annotations: Optional[dict] = None


class ConfigMapMetaData(BaseModel):
    name: str
    namespace: Optional[str] = None


class SecretMetaData(ConfigMapMetaData):
    pass


class Port(BaseModel):
    containerPort: int
    name: Optional[str] = None
    protocol: Literal["TCP", " UDP", "SCTP"] = "TCP"
    hostPort: Optional[int] = None
    hostIP: Optional[str] = None
