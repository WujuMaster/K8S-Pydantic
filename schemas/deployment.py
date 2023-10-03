from typing import List, Optional, Union

from pydantic import BaseModel

from .common import DeploymentMetaData, LabelSelector, PodMetaData, Port


class ContainerConfigMapRef(BaseModel):
    name: str


class ContainerSecretRef(BaseModel):
    name: str


class ContainerEnvSource(BaseModel):
    configMapRef: Optional[ContainerConfigMapRef] = None


class ContainerSecretSource(BaseModel):
    secretRef: Optional[ContainerSecretRef] = None


class ContainerEnv(BaseModel):
    name: str
    value: str


class ContainerVolumeMount(BaseModel):
    name: str
    mountPath: str
    readOnly: Optional[bool] = None


class Container(BaseModel):
    name: str
    image: Optional[str] = None
    imagePullPolicy: str = "Always"
    ports: Optional[List[Port]] = None
    envFrom: Optional[List[Union[ContainerEnvSource, ContainerSecretSource]]] = None
    env: Optional[List[ContainerEnv]] = None
    volumeMounts: Optional[List[ContainerVolumeMount]] = None


class DeploymentVolumeConfigMap(BaseModel):
    name: str


class DeploymentVolume(BaseModel):
    name: str
    configMap: DeploymentVolumeConfigMap


class PodSpec(BaseModel):
    containers: List[Container]
    volumes: Optional[List[DeploymentVolume]] = None


class DeploymentTemplate(BaseModel):
    metadata: PodMetaData
    spec: PodSpec


class DeploymentStrategy(BaseModel):
    type: str
    rollingUpdate: Optional[dict] = None


class DeploymentSpec(BaseModel):
    replicas: int = 1
    selector: LabelSelector
    template: DeploymentTemplate
    strategy: Optional[DeploymentStrategy] = None


class Deployment(BaseModel):
    apiVersion: str = "apps/v1"
    kind: str = "Deployment"
    metadata: DeploymentMetaData
    spec: DeploymentSpec
