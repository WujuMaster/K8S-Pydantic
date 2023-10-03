from typing import Any, Dict

from pydantic import BaseModel

from .common import SecretMetaData


class Secret(BaseModel):
    apiVersion: str = "v1"
    kind: str = "Secret"
    metadata: SecretMetaData
    type: str = "Opaque"
    data: Dict[str, str]
