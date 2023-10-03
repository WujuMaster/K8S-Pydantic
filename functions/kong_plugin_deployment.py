import yaml

import schemas as k8s


def create_kong_deployment(
    ingress_conf: k8s.IngressConf,
    output_path: str,
):
    yaml_config: str = ""
    kong_plugin = k8s.Deployment(
        metadata=k8s.DeploymentMetaData(
            name="ingress-kong",
            namespace="kong",
            labels={"app": "ingress-kong"},
        ),
        spec=k8s.DeploymentSpec(
            selector=k8s.LabelSelector(matchLabels={"app": "kong"}),
            template=k8s.DeploymentTemplate(
                metadata=k8s.PodMetaData(labels={"app": "kong"}),
                spec=k8s.PodSpec(
                    containers=[
                        k8s.Container(
                            name="proxy",
                            env=[
                                k8s.ContainerEnv(
                                    name="KONG_PLUGINS",
                                    value=f"{ingress_conf.plugin.name}",
                                ),
                                k8s.ContainerEnv(
                                    name="KONG_LUA_PACKAGE_PATH",
                                    value="/opt/?.lua;;",
                                ),
                            ],
                            volumeMounts=[
                                k8s.ContainerVolumeMount(
                                    name=f"kong-plugin-{ingress_conf.plugin.name}",
                                    mountPath=f"/opt/{ingress_conf.className}/plugins/{ingress_conf.plugin.name}",
                                ),
                            ],
                        )
                    ],
                    volumes=[
                        k8s.DeploymentVolume(
                            name=f"kong-plugin-{plugin_name}",
                            configMap=k8s.DeploymentVolumeConfigMap(
                                name=f"kong-plugin-{plugin_name}"
                            ),
                        )
                        for plugin_name in ingress_conf.plugin.name.split(",")
                    ],
                ),
            ),
        ),
    )
    yaml_config += yaml.dump(kong_plugin.model_dump(exclude_none=True)) + "\n---\n"

    with open(output_path, "a") as outfile:
        outfile.write(yaml_config)
