from typing import Dict, List, Literal

from pydantic import BaseModel

from .common import ServiceMetaData


class ServicePort(BaseModel):
    port: int
    targetPort: int
    name: str = "http"
    protocol: Literal["TCP", " UDP", "SCTP"] = "TCP"


class ServiceSpec(BaseModel):
    selector: Dict[str, str]
    ports: List[ServicePort]
    type: Literal["ClusterIP", "LoadBalancer", "NodePort", "ExternalName"] = "ClusterIP"


class Service(BaseModel):
    apiVersion: str = "v1"
    kind: str = "Service"
    metadata: ServiceMetaData
    spec: ServiceSpec
