import yaml

import schemas as k8s


def create_deployments(
    applications_conf: k8s.ApplicationConfList,
    shared_conf: k8s.SharedConf,
    output_path: str,
):
    yaml_config: str = ""
    for app_conf in applications_conf.applications:
        deployment = k8s.Deployment(
            metadata=k8s.DeploymentMetaData(
                name=app_conf.name,
                namespace=shared_conf.namespace,
                labels={"deployment": app_conf.name},
            ),
            spec=k8s.DeploymentSpec(
                replicas=app_conf.deployment.replicas or shared_conf.replicas,
                selector=k8s.LabelSelector(matchLabels={"pod": app_conf.name}),
                template=k8s.DeploymentTemplate(
                    metadata=k8s.PodMetaData(labels={"pod": app_conf.name}),
                    spec=k8s.PodSpec(
                        containers=[
                            k8s.Container(
                                name=app_conf.name,
                                image=f"{shared_conf.image.registry}/{app_conf.image.repository}:{app_conf.image.tag}",
                                ports=[
                                    k8s.Port(containerPort=app_conf.image.containerPort)
                                ],
                                envFrom=[
                                    k8s.ContainerEnvSource(
                                        configMapRef=k8s.ContainerConfigMapRef(
                                            name=f"{app_conf.name}-configmap"
                                        )
                                    ),
                                    k8s.ContainerSecretSource(
                                        secretRef=k8s.ContainerSecretRef(
                                            name=f"{app_conf.name}-secret"
                                        ),
                                    ),
                                ],
                            )
                        ]
                    ),
                ),
            ),
        )

        yaml_config += yaml.dump(deployment.model_dump(exclude_none=True)) + "\n---\n"

    with open(output_path, "w") as outfile:
        outfile.write(yaml_config)
