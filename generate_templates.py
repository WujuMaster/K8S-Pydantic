import yaml

import schemas as k8s
from functions import (
    create_configmaps_and_secrets,
    create_deployments,
    create_ingress,
    create_kong_deployment,
    create_services,
)

INPUT_DIR = "values"
OUTPUT_DIR = "templates"


if __name__ == "__main__":
    with open(f"{INPUT_DIR}/shared.yaml", "r") as file:
        shared_conf = k8s.SharedConf(**yaml.safe_load(file))

    with open(f"{INPUT_DIR}/applications.yaml", "r") as file:
        applications_conf = k8s.ApplicationConfList(**yaml.safe_load(file))

    with open(f"{INPUT_DIR}/ingress.yaml", "r") as file:
        ingress_conf = k8s.IngressConf(**yaml.safe_load(file))

    create_services(
        applications_conf=applications_conf,
        shared_conf=shared_conf,
        output_path=f"{OUTPUT_DIR}/services.yaml",
    )
    create_configmaps_and_secrets(
        applications_conf=applications_conf,
        shared_conf=shared_conf,
        output_configmap_path=f"{OUTPUT_DIR}/configmaps.yaml",
        output_secret_path=f"{OUTPUT_DIR}/secrets.yaml",
    )
    create_deployments(
        applications_conf=applications_conf,
        shared_conf=shared_conf,
        output_path=f"{OUTPUT_DIR}/deployments.yaml",
    )
    create_kong_deployment(
        ingress_conf=ingress_conf,
        output_path=f"{OUTPUT_DIR}/deployments.yaml",
    )
    create_ingress(
        applications_conf=applications_conf,
        shared_conf=shared_conf,
        ingress_conf=ingress_conf,
        output_path=f"{OUTPUT_DIR}/ingress.yaml",
    )
