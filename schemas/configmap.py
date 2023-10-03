from typing import Any, Dict

from pydantic import BaseModel

from .common import ConfigMapMetaData


class ConfigMap(BaseModel):
    apiVersion: str = "v1"
    kind: str = "ConfigMap"
    metadata: ConfigMapMetaData
    data: Dict[str, Any]
