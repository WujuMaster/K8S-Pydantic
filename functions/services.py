import yaml

import schemas as k8s


def create_services(
    applications_conf: k8s.ApplicationConfList,
    shared_conf: k8s.SharedConf,
    output_path: str,
):
    yaml_config: str = ""
    for app_conf in applications_conf.applications:
        service = k8s.Service(
            metadata=k8s.ServiceMetaData(
                name=app_conf.name,
                namespace=shared_conf.namespace,
                labels={"service": app_conf.name},
            ),
            spec=k8s.ServiceSpec(
                selector={"pod": app_conf.name},
                ports=[
                    k8s.ServicePort(
                        port=app_conf.service.port,
                        targetPort=app_conf.image.containerPort,
                    )
                ],
            ),
        )

        yaml_config += yaml.dump(service.model_dump(exclude_none=True)) + "\n---\n"

    with open(output_path, "w") as outfile:
        outfile.write(yaml_config)
