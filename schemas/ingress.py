from typing import List, Optional, Literal

from pydantic import BaseModel

from .common import IngressMetaData


class IngressRulePath(BaseModel):
    path: Optional[str]
    pathType: Optional[str] = "Prefix"
    backend: dict


class HttpBackendServicePort(BaseModel):
    number: int = 80


class HttpBackendService(BaseModel):
    name: str
    port: HttpBackendServicePort


class HttpBackend(BaseModel):
    service: HttpBackendService


class HttpPath(BaseModel):
    path: str
    pathType: Literal["Exact", "ImplementationSpecific", "Prefix"] = "Prefix"
    backend: HttpBackend


class HttpRule(BaseModel):
    paths: List[HttpPath]


class IngressRule(BaseModel):
    host: Optional[str] = None
    http: HttpRule


class IngressTLS(BaseModel):
    hosts: List[str]
    secretName: str


class IngressSpec(BaseModel):
    ingressClassName: str = "kong"
    rules: List[IngressRule]
    tls: Optional[IngressTLS] = None


class IngressBackend(BaseModel):
    serviceName: str
    servicePort: int


class Ingress(BaseModel):
    apiVersion: str = "networking.k8s.io/v1"
    kind: str = "Ingress"
    metadata: IngressMetaData
    spec: IngressSpec
