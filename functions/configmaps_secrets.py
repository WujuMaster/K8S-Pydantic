import os

import yaml
from dotenv import load_dotenv

import schemas as k8s

from .utils import encode_base64


def create_configmaps_and_secrets(
    applications_conf: k8s.ApplicationConfList,
    shared_conf: k8s.SharedConf,
    output_configmap_path: str,
    output_secret_path: str,
):
    yaml_configmap: str = ""
    yaml_secret: str = ""

    for app_conf in applications_conf.applications:
        load_dotenv(
            dotenv_path=os.path.join(os.getcwd(), f".env.{app_conf.name}"),
            override=True,
        )
        env_dict = dict(os.environ)
        configmap = k8s.ConfigMap(
            metadata=k8s.ConfigMapMetaData(
                name=f"{app_conf.name}-configmap",
                namespace=shared_conf.namespace,
            ),
            data={k: v for k, v in env_dict.items() if k in app_conf.env},
        )
        secret = k8s.Secret(
            metadata=k8s.SecretMetaData(
                name=f"{app_conf.name}-secret",
                namespace=shared_conf.namespace,
            ),
            data={
                k: encode_base64(v) for k, v in env_dict.items() if k in app_conf.secret
            },
        )

        yaml_configmap += yaml.dump(configmap.model_dump(exclude_none=True)) + "\n---\n"
        yaml_secret += yaml.dump(secret.model_dump(exclude_none=True)) + "\n---\n"

    with open(output_configmap_path, "w") as outfile:
        outfile.write(yaml_configmap)

    with open(output_secret_path, "w") as outfile:
        outfile.write(yaml_secret)
